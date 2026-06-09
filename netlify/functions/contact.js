/* Netlify Function: Kontaktformular via Brevo API
   API Key wird als Netlify-Umgebungsvariable gesetzt: BREVO_API_KEY
*/

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

  const { name, email, phone, subject, message, object: propertyObject, privacy } = data;

  if (!name || !email || !message || !privacy) {
    return { statusCode: 400, body: 'Pflichtfelder fehlen' };
  }

  const apiKey = process.env.BREVO_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: 'Konfigurationsfehler' };
  }

  const emailBody = `
Neue Anfrage über attergauer-wohnbau.at

Name:     ${name}
E-Mail:   ${email}
Telefon:  ${phone || '—'}
Betreff:  ${subject || '—'}
Objekt:   ${propertyObject || '—'}

Nachricht:
${message}
  `.trim();

  // Send notification to company
  const payload = {
    sender: { name: 'Attergauer Wohnbau Website', email: 'noreply@attergauer-wohnbau.at' },
    to: [{ email: 'team@attergauer-wohnbau.at', name: 'Attergauer Wohnbau' }],
    replyTo: { email, name },
    subject: `Neue Anfrage: ${subject || propertyObject || 'Kontaktformular'}`,
    textContent: emailBody,
  };

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'api-key': apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errText = await res.text();
      console.error('Brevo error:', errText);
      return { statusCode: 500, body: 'E-Mail-Versand fehlgeschlagen' };
    }

    // Send confirmation to inquirer
    const confirm = {
      sender: { name: 'Attergauer Wohnbau GmbH', email: 'team@attergauer-wohnbau.at' },
      to: [{ email, name }],
      subject: 'Ihre Anfrage bei Attergauer Wohnbau GmbH',
      textContent: `Sehr geehrte/r ${name},\n\nvielen Dank für Ihre Anfrage. Wir werden uns so schnell wie möglich bei Ihnen melden.\n\nMit freundlichen Grüßen\nAttergauer Wohnbau GmbH\nThern 20, 4880 St. Georgen i. A.\nTel.: +43 7667 6409-42\nteam@attergauer-wohnbau.at`,
    };

    await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: { 'api-key': apiKey, 'Content-Type': 'application/json' },
      body: JSON.stringify(confirm),
    });

    return { statusCode: 200, body: 'OK' };
  } catch (err) {
    console.error('Function error:', err);
    return { statusCode: 500, body: 'Serverfehler' };
  }
};
