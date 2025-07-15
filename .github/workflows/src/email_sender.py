import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_podcast_email(self, recipient_email, podcast_data):
        """Envoie l'email avec le podcast"""
        try:
            # Créer le message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"🎙️ Podcast Actualités Madagascar - {datetime.now().strftime('%d/%m/%Y')}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Contenu HTML de l'email
            html_content = self._create_html_content(podcast_data)
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Contenu texte de l'email
            text_content = self._create_text_content(podcast_data)
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)
            
            # Envoyer l'email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✅ Email envoyé à {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur envoi email: {e}")
            return False
    
    def _create_html_content(self, podcast_data):
        """Crée le contenu HTML de l'email"""
        audio_url = podcast_data['audio_generation']['generated_audios'][0]['audio_urls'][0]
        duration = podcast_data['audio_generation']['generated_audios'][0]['audio_durations'][0]
        poster_url = podcast_data.get('poster_url', '')
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
            <div style="background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50; margin-bottom: 5px;">🎙️ Actualités Madagascar</h1>
                    <p style="color: #7f8c8d; font-size: 16px; margin: 0;">Podcast quotidien - {datetime.now().strftime('%d/%m/%Y')}</p>
                </div>
                
                <div style="text-align: center; margin-bottom: 30px;">
                    <img src="{poster_url}" alt="Podcast Cover" style="width: 200px; height: 200px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                </div>
                
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 30px; border-left: 4px solid #3498db;">
                    <h2 style="color: #2c3e50; margin-top: 0; margin-bottom: 15px;">📰 {podcast_data['podcast_name']}</h2>
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                        <p style="margin: 0;"><strong>⏱️ Durée:</strong> {duration // 60} min {duration % 60} sec</p>
                        <p style="margin: 0;"><strong>🎭 Présentateurs:</strong> Puck et Kore</p>
                        <p style="margin: 0;"><strong>🌍 Langue:</strong> Français</p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 40px 0;">
                    <a href="{audio_url}" 
                       style="display: inline-block; background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 18px 40px; 
                              text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; 
                              box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3); transition: all 0.3s ease;">
                        🎧 Écouter le Podcast
                    </a>
                </div>
                
                <div style="background-color: #ecf0f1; padding: 20px; border-radius: 8px; margin-top: 30px;">
                    <h3 style="color: #2c3e50; margin-top: 0; margin-bottom: 15px;">📋 Liens utiles</h3>
                    <p style="margin: 8px 0;"><a href="{podcast_data.get('script_url', '#')}" style="color: #3498db; text-decoration: none;">📝 Script complet du podcast</a></p>
                    <p style="margin: 8px 0;"><a href="https://actu.orange.mg" style="color: #3498db; text-decoration: none;">🌐 Source: Orange Actu Madagascar</a></p>
                    <p style="margin: 8px 0;"><a href="https://github.com/ahaulkory/madagascar-news-automation" style="color: #3498db; text-decoration: none;">⚙️ Automatisation GitHub</a></p>
                </div>
                
                <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                    <p style="color: #7f8c8d; font-size: 12px; margin: 0;">
                        📡 Podcast généré automatiquement le {datetime.now().strftime('%d/%m/%Y à %H:%M')} (CET)
                    </p>
                    <p style="color: #95a5a6; font-size: 11px; margin: 5px 0 0 0;">
                        Système d'automatisation GitHub Actions
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _create_text_content(self, podcast_data):
        """Crée le contenu texte de l'email"""
        audio_url = podcast_data['audio_generation']['generated_audios'][0]['audio_urls'][0]
        duration = podcast_data['audio_generation']['generated_audios'][0]['audio_durations'][0]
        
        return f"""
🎙️ ACTUALITÉS MADAGASCAR - {datetime.now().strftime('%d/%m/%Y')}

═══════════════════════════════════════════════════════════════

📰 {podcast_data['podcast_name']}

📊 DÉTAILS:
⏱️ Durée: {duration // 60} min {duration % 60} sec
🎭 Présentateurs: Puck et Kore
🌍 Langue: Français
📅 Généré le: {datetime.now().strftime('%d/%m/%Y à %H:%M')} (CET)

🎧 ÉCOUTER:
{audio_url}

📋 LIENS UTILES:
📝 Script complet: {podcast_data.get('script_url', 'Non disponible')}
🌐 Source: https://actu.orange.mg
⚙️ Automatisation: https://github.com/ahaulkory/madagascar-news-automation

═══════════════════════════════════════════════════════════════

📡 Ce podcast est généré automatiquement chaque jour à 11h00 CET
   via GitHub Actions. Pour plus d'informations, consultez le repository.

Bonne écoute ! 🎵
        """
