import os
import sys
from datetime import datetime
from news_scraper import NewsScraper
from podcast_generator import PodcastGenerator
from email_sender import EmailSender

def main():
    print("🚀 Démarrage de l'automatisation du podcast Madagascar...")
    
    try:
        # Configuration
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        recipient_email = os.environ.get('RECIPIENT_EMAIL')
        
        if not all([sender_email, sender_password, recipient_email]):
            raise ValueError("Variables d'environnement manquantes")
        
        # 1. Scraper les actualités
        print("📰 Scraping des actualités...")
        scraper = NewsScraper()
        news_content = scraper.scrape_orange_mg()
        
        if not news_content:
            print("❌ Échec du scraping")
            return False
        
        # 2. Générer le podcast
        print("🎙️ Génération du podcast...")
        generator = PodcastGenerator()
        podcast_data = generator.create_podcast(news_content)
        
        if not podcast_data:
            print("❌ Échec de la génération du podcast")
            return False
        
        # 3. Envoyer par email
        print("📧 Envoi par email...")
        email_sender = EmailSender(sender_email, sender_password)
        success = email_sender.send_podcast_email(recipient_email, podcast_data)
        
        if success:
            print("✅ Podcast envoyé avec succès!")
            return True
        else:
            print("❌ Échec de l'envoi email")
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
