/* Netlify Function: Kontaktformular via Brevo API
   API Key wird als Netlify-Umgebungsvariable gesetzt: BREVO_API_KEY
   NIEMALS den API Key in dieses File schreiben!

   Brevo Listen:
     #2 = AWB Weißenkirchen
     #3 = AWB Nußdorf 8
     #4 = Allgemeine Anfragen / Maklerei
     #5 = NewsletterAWB

   Eigenprojekte (Seeblick Nußdorf, Reihenhäuser Weißenkirchen)
   → zusätzlich Deal in Pipeline "Attergauer Wohnbau", Stage "Neue Anfrage"
*/

// ---------------------------------------------------------------------------
// Hilfsfunktion: Brevo API Call
// ---------------------------------------------------------------------------
async function brevo(apiKey, method, path, body) {
  const res = await fetch(`https://api.brevo.com/v3${path}`, {
    method,
    headers: {
      'api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try { data = JSON.parse(text); } catch { data = text; }
  return { ok: res.ok, status: res.status, data };
}

// ---------------------------------------------------------------------------
// Welche Brevo-Liste passt zum Objekt?
// ---------------------------------------------------------------------------
function getListId(obj) {
  if (!obj) return 4;
  if (obj.includes('Seeblick') || obj.includes('Nußdorf 8')) return 3;
  if (obj.includes('Weißenkirchen')) return 2;
  return 4;
}

// ---------------------------------------------------------------------------
// Ist es ein Eigenprojekt? → Deal anlegen
// ---------------------------------------------------------------------------
function isEigenprojekt(obj) {
  if (!obj) return false;
  return obj.includes('Seeblick') || obj.includes('Weißenkirchen');
}

// ---------------------------------------------------------------------------
// Pipeline-ID und Stage-ID "Neue Anfrage" aus Brevo holen
// ---------------------------------------------------------------------------
async function getPipelineStage(apiKey) {
  const { ok, data } = await brevo(apiKey, 'GET', '/crm/pipeline/details/all');
  if (!ok || !Array.isArray(data)) return null;

  const pipeline = data.find(p =>
    p.pipeline_name && p.pipeline_name.toLowerCase().includes('attergauer')
  );
  if (!pipeline) return null;

  const stages = pipeline.stages || [];
  const stage = stages.find(s =>
    s.name && s.name.toLowerCase().includes('neue anfrage')
  );

  return {
    pipelineId: pipeline.id,
    stageId: stage ? stage.id : (stages[0] ? stages[0].id : null),
  };
}

// ---------------------------------------------------------------------------
// Handler
// ---------------------------------------------------------------------------
exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  let data;
  try {
    data = JSON.parse(event.body);
  } catch {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const {
    hp_website,
    recaptchaToken,
    name,
    email,
    phone,
    subject,
    message,
    object: propertyObject,
    privacy,
    newsletter,
    interesse_miete,
    interesse_mietkauf_belags,
    interesse_mietkauf_schluessel,
  } = data;

  // Honeypot: Bots füllen dieses versteckte Feld aus
  if (hp_website) {
    return { statusCode: 200, body: 'OK' };
  }

  // reCAPTCHA v3 verifizieren — kein Token = sofort blockieren
  const recaptchaSecret = process.env.RECAPTCHA_SECRET_KEY;
  if (!recaptchaToken) {
    return { statusCode: 200, body: 'OK' };
  }
  if (recaptchaSecret) {
    try {
      const verifyRes = await fetch(
        `https://www.google.com/recaptcha/api/siteverify?secret=${recaptchaSecret}&response=${recaptchaToken}`,
        { method: 'POST' }
      );
      const verifyData = await verifyRes.json();
      if (!verifyData.success || verifyData.score < 0.3) {
        return { statusCode: 400, body: 'Captcha fehlgeschlagen' };
      }
    } catch (err) {
      // Bei API-Fehler: Anfrage trotzdem durchlassen
    }
  }

  if (!name || !email || !phone || !message || !privacy) {
    return { statusCode: 400, body: 'Pflichtfelder fehlen' };
  }

const apiKey = process.env.BREVO_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: 'Konfigurationsfehler' };
  }

  // -------------------------------------------------------------------------
  // 1. E-Mail an Team
  // -------------------------------------------------------------------------
  const emailBody = `
Neue Anfrage über attergauer-wohnbau.at

Name:     ${name}
E-Mail:   ${email}
Telefon:  ${phone || '—'}
Betreff:  ${subject || '—'}
Objekt:   ${propertyObject || '—'}
Newsletter: ${newsletter ? 'Ja' : 'Nein'}

Nachricht:
${message}
  `.trim();

  const teamMail = {
    sender: { name: 'Attergauer Wohnbau Website', email: 'noreply@attergauer-wohnbau.at' },
    to: [
      { email: 'team@attergauer-wohnbau.at', name: 'Attergauer Wohnbau' },
      { email: 'michael@attergauer-wohnbau.at', name: 'Michael Schönleitner' },
    ],
    replyTo: { email, name },
    subject: `Neue Anfrage: ${subject || propertyObject || 'Kontaktformular'}`,
    textContent: emailBody,
  };

  try {
    const mailRes = await brevo(apiKey, 'POST', '/smtp/email', teamMail);
    if (!mailRes.ok) {
      console.error('Team-Mail Fehler:', mailRes.data);
      return { statusCode: 500, body: 'E-Mail-Versand fehlgeschlagen' };
    }
  } catch (err) {
    console.error('Team-Mail Exception:', err);
    return { statusCode: 500, body: 'Serverfehler' };
  }

  // -------------------------------------------------------------------------
  // 2. Bestätigungs-E-Mail an Anfragenden (mit Exposé-Links je nach Projekt)
  // -------------------------------------------------------------------------
  const BASE_URL = 'https://www.attergauer-wohnbau.at';

  // Exposé-Links zusammenstellen
  const exposeLinks = [];
  if (propertyObject && propertyObject.includes('Seeblick')) {
    exposeLinks.push(`Exposé Seeblick Häuser Nußdorf:\n${BASE_URL}/downloads/expose-seeblick-nussdorf.pdf`);
  }
  if (propertyObject && propertyObject.includes('Weißenkirchen')) {
    if (interesse_miete) {
      exposeLinks.push(`Exposé Miete:\n${BASE_URL}/downloads/expose-weissenkirchen-miete.pdf`);
    }
    if (interesse_mietkauf_belags) {
      exposeLinks.push(`Exposé Mietkauf belagsfertig:\n${BASE_URL}/downloads/expose-weissenkirchen-mietkauf-belags.pdf`);
    }
    if (interesse_mietkauf_schluessel) {
      exposeLinks.push(`Exposé Mietkauf schlüsselfertig:\n${BASE_URL}/downloads/expose-weissenkirchen-mietkauf-schluessel.pdf`);
    }
    // Falls kein Interesse angekreuzt: alle drei mitschicken
    if (!interesse_miete && !interesse_mietkauf_belags && !interesse_mietkauf_schluessel) {
      exposeLinks.push(`Exposé Miete:\n${BASE_URL}/downloads/expose-weissenkirchen-miete.pdf`);
      exposeLinks.push(`Exposé Mietkauf belagsfertig:\n${BASE_URL}/downloads/expose-weissenkirchen-mietkauf-belags.pdf`);
      exposeLinks.push(`Exposé Mietkauf schlüsselfertig:\n${BASE_URL}/downloads/expose-weissenkirchen-mietkauf-schluessel.pdf`);
    }
  }
  if (propertyObject && propertyObject.includes('Baugrundstück')) {
    exposeLinks.push(`Exposé Baugrundstück Nußdorf:\n${BASE_URL}/downloads/expose-grundstueck-nussdorf.pdf`);
  }

  const exposeSection = exposeLinks.length > 0
    ? `\n\nAls kleines Dankeschön finden Sie hier ${exposeLinks.length === 1 ? 'Ihr Exposé' : 'Ihre Exposés'} zum Download:\n\n${exposeLinks.join('\n\n')}`
    : '';

  const confirmMail = {
    sender: { name: 'Attergauer Wohnbau GmbH', email: 'team@attergauer-wohnbau.at' },
    to: [{ email, name }],
    subject: 'Ihre Anfrage bei Attergauer Wohnbau GmbH',
    textContent: `Sehr geehrte/r ${name},\n\nvielen Dank für Ihre Anfrage. Wir werden uns so schnell wie möglich bei Ihnen melden.${exposeSection}\n\nMit freundlichen Grüßen\nAttergauer Wohnbau GmbH\nThern 20, 4880 St. Georgen i. A.\nTel.: +43 7667 6409-42\nteam@attergauer-wohnbau.at`,
  };

  await brevo(apiKey, 'POST', '/smtp/email', confirmMail).catch(err =>
    console.error('Bestätigungs-Mail Fehler:', err)
  );

  // -------------------------------------------------------------------------
  // 3. CRM: Kontakt anlegen / aktualisieren
  //    updateEnabled:true → existierender Kontakt wird aktualisiert statt Fehler
  // -------------------------------------------------------------------------
  const listId = getListId(propertyObject);
  const listIds = [listId];
  if (newsletter) listIds.push(5); // NewsletterAWB

  // Kontakt anlegen / aktualisieren
  const contactPayload = {
    email,
    updateEnabled: true,
    attributes: {
      NAME: name,
      TEL: phone || '',
    },
    listIds,
  };
  await brevo(apiKey, 'POST', '/contacts', contactPayload);

  // Listen explizit setzen
  for (const lid of listIds) {
    await brevo(apiKey, 'POST', `/contacts/lists/${lid}/contacts/add`, { emails: [email] });
  }

  // -------------------------------------------------------------------------
  // 4. Deal anlegen (für alle Anfragen)
  // -------------------------------------------------------------------------
  try {
      const pipelineInfo = await getPipelineStage(apiKey);

      if (pipelineInfo) {
        const dealName = `${name} – ${propertyObject}`;
        const dealPayload = {
          name: dealName,
          attributes: {
            pipeline: pipelineInfo.pipelineId,
            deal_stage: pipelineInfo.stageId,
          },
        };

        const dealRes = await brevo(apiKey, 'POST', '/crm/deals', dealPayload);

        if (dealRes.ok && dealRes.data && dealRes.data.id) {
          const dealId = dealRes.data.id;

          // Kontakt-ID holen und mit Deal verknüpfen
          const contactRes = await brevo(apiKey, 'GET', `/contacts/${encodeURIComponent(email)}`);
          let debugInfo = { contactStatus: contactRes.status, contactId: contactRes.data?.id };
          if (contactRes.ok && contactRes.data && contactRes.data.id) {
            const linkRes = await brevo(apiKey, 'PATCH', `/crm/deals/${dealId}/link-unlink`, {
              linkContactIds: [parseInt(contactRes.data.id)],
            });
            debugInfo.linkStatus = linkRes.status;
            debugInfo.linkData = linkRes.data;
          }
          debugInfo.dealId = dealId;

          // Nachricht als Notiz im Deal hinterlegen
          if (message) {
            await brevo(apiKey, 'POST', '/crm/notes', {
              text: message,
              dealIds: [dealId],
            }).catch(err => console.error('Notiz Fehler:', err));
          }
        } else {
          console.error('Deal anlegen Fehler:', dealRes.data);
        }
      } else {
        console.error('Pipeline "Attergauer Wohnbau" nicht gefunden');
      }
  } catch (err) {
    console.error('Deal Exception:', err);
  }

  return { statusCode: 200, body: JSON.stringify({ ok: true, debug: typeof debugInfo !== 'undefined' ? debugInfo : null }) };
};
