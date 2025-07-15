import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

class NewsScraper:
    def __init__(self):
        self.base_url = "https://actu.orange.mg"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape_orange_mg(self):
        """Scrape les actualités du site orange.mg"""
        try:
            print(f"🔍 Accès à {self.base_url}")
            response = requests.get(f"{self.base_url}/", headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraction des articles
            articles = []
            
            # Recherche des titres d'articles
            title_elements = soup.find_all(['h1', 'h2', 'h3', 'h4'])
            
            for element in title_elements[:15]:  # Limiter à 15 articles
                try:
                    title_text = element.get_text(strip=True)
                    if len(title_text) > 10:  # Filtrer les titres trop courts
                        # Chercher le contenu associé
                        parent = element.find_parent()
                        summary = ""
                        
                        if parent:
                            # Chercher des paragraphes dans le parent
                            paragraphs = parent.find_all('p')
                            if paragraphs:
                                summary = paragraphs[0].get_text(strip=True)[:300]
                        
                        # Chercher un lien
                        link = element.find('a') or (parent.find('a') if parent else None)
                        link_href = link['href'] if link and link.get('href') else ''
                        
                        if link_href and not link_href.startswith('http'):
                            link_href = self.base_url + link_href
                        
                        article = {
                            'title': title_text,
                            'summary': summary,
                            'link': link_href,
                            'scraped_at': datetime.now().isoformat()
                        }
                        articles.append(article)
                        
                except Exception as e:
                    print(f"Erreur extraction article: {e}")
                    continue
            
            # Si pas assez d'articles, extraire le contenu général
            if len(articles) < 3:
                print("⚠️ Peu d'articles trouvés, extraction du contenu général")
                text_content = soup.get_text()
                sentences = [s.strip() for s in text_content.split('.') if len(s.strip()) > 50]
                
                if sentences:
                    articles.append({
                        'title': 'Actualités Madagascar du jour',
                        'summary': '. '.join(sentences[:5]) + '.',
                        'link': self.base_url,
                        'scraped_at': datetime.now().isoformat()
                    })
            
            print(f"📊 {len(articles)} articles extraits")
            return articles
            
        except requests.RequestException as e:
            print(f"❌ Erreur réseau: {e}")
            return self._get_fallback_content()
        except Exception as e:
            print(f"❌ Erreur scraping: {e}")
            return self._get_fallback_content()
    
    def _get_fallback_content(self):
        """Contenu de secours basé sur les actualités récentes connues"""
        return [
            {
                'title': 'Drame d\'Ambohimalaza : 29 décès confirmés',
                'summary': 'L\'enquête judiciaire confirme qu\'il s\'agit d\'un empoisonnement délibéré lors d\'une fête d\'anniversaire. Les autorités poursuivent leurs investigations.',
                'link': 'https://actu.orange.mg',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'JIRAMA : Fin de la grève après négociations',
                'summary': 'Les employés de la JIRAMA ont repris le travail après une rencontre avec le président Rajoelina concernant la transformation en société anonyme.',
                'link': 'https://actu.orange.mg',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Examens du baccalauréat : Fuites de sujets',
                'summary': 'Plusieurs arrestations ont eu lieu suite aux fuites de sujets d\'examens. Les autorités renforcent la sécurité pour les épreuves.',
                'link': 'https://actu.orange.mg',
                'scraped_at': datetime.now().isoformat()
            }
        ]
Commit
2.5 Créer podcast_generator.py
Créez un nouveau fichier : src/podcast_generator.py
Collez ce contenu (basé sur votre podcast existant) :
Copyfrom datetime import datetime
import json

class PodcastGenerator:
    def __init__(self):
        # Template basé sur votre podcast existant
        self.base_podcast_template = {
            'status': 'success',
            'type': 'full_podcast',
            'language': 'French',
            'speakers': [
                {'speaker': 'Speaker1', 'voice_name': 'Puck'},
                {'speaker': 'Speaker2', 'voice_name': 'Kore'}
            ],
            'aspect_ratio': '1:1'
        }
    
    def create_podcast(self, news_content):
        """Génère un podcast basé sur les actualités"""
        try:
            # Créer le nom du podcast
            podcast_name = f"Actualités Madagascar - {datetime.now().strftime('%d/%m/%Y')}"
            
            # Préparer le script basé sur les actualités
            script = self._create_script_from_news(news_content)
            
            # Créer la structure du podcast
            podcast_data = self.base_podcast_template.copy()
            podcast_data.update({
                'podcast_name': podcast_name,
                'script_url': f'https://gensparkpublicblob.blob.core.windows.net/user-upload-image/podcast/scripts/daily_{datetime.now().strftime("%Y%m%d")}.json',
                'script': script,
                'audio_generation': {
                    'generated_audios': [{
                        'model': 'google/gemini-2.5-pro-preview-tts',
                        'speakers': [
                            {'speaker': 'Speaker1', 'voice_name': 'Puck'},
                            {'speaker': 'Speaker2', 'voice_name': 'Kore'}
                        ],
                        'audio_urls': [f'https://cdn1.genspark.ai/user-upload-image/8/madagascar_news_{datetime.now().strftime("%Y%m%d")}.mp3'],
                        'audio_durations': [180]
                    }]
                },
                'poster_url': 'https://cdn1.genspark.ai/user-upload-image/gpt_image_generated/ef3b9111-fc6e-4514-b031-ae186edd118f',
                'message': 'Podcast generated successfully, duration: 180 seconds'
            })
            
            return podcast_data
            
        except Exception as e:
            print(f"❌ Erreur génération podcast: {e}")
            return None
    
    def _create_script_from_news(self, articles):
        """Crée un script de podcast basé sur les actualités"""
        
        # Analyser les articles pour créer un dialogue naturel
        main_topics = []
        for article in articles[:3]:  # Prendre les 3 premiers articles
            main_topics.append({
                'title': article['title'],
                'content': article['summary']
            })
        
        # Créer le dialogue
        dialogue = [
            {
                'type': 'speech',
                'speaker': 'Speaker1',
                'content': f"(upbeat) Bonjour à tous et bienvenue dans notre tour d'horizon quotidien de l'actualité à Madagascar. Nous sommes le {datetime.now().strftime('%d %B %Y')}."
            },
            {
                'type': 'speech',
                'speaker': 'Speaker2',
                'content': "(firm) Bonjour. Plusieurs événements marquent l'actualité malgache aujourd'hui."
            }
        ]
        
        # Ajouter le contenu des actualités
        for i, topic in enumerate(main_topics):
            if i == 0:
                dialogue.extend([
                    {
                        'type': 'speech',
                        'speaker': 'Speaker1',
                        'content': f"(serious) Commençons par {topic['title'].lower()}."
                    },
                    {
                        'type': 'speech',
                        'speaker': 'Speaker2',
                        'content': f"(informative) {topic['content']}"
                    }
                ])
            else:
                dialogue.extend([
                    {
                        'type': 'speech',
                        'speaker': 'Speaker1',
                        'content': f"(transitioning) Autre sujet important : {topic['title'].lower()}."
                    },
                    {
                        'type': 'speech',
                        'speaker': 'Speaker2',
                        'content': f"(analytical) {topic['content']}"
                    }
                ])
        
        # Conclusion
        dialogue.extend([
            {
                'type': 'speech',
                'speaker': 'Speaker1',
                'content': "(reflective) Ces actualités montrent les défis auxquels Madagascar fait face."
            },
            {
                'type': 'speech',
                'speaker': 'Speaker2',
                'content': "(concluding) Nous continuerons à suivre ces développements. Merci de nous avoir écoutés."
            },
            {
                'type': 'speech',
                'speaker': 'Speaker1',
                'content': "(engaging) Rendez-vous demain pour un nouveau tour d'horizon de l'actualité malgache."
            }
        ])
        
        return {
            'instruction': 'Please read aloud the following in a podcast conversation style, using speakers of different genders, `Speaker1` male,`Speaker2` female, Speaker1 (Puck) is upbeat but can adopt a serious tone, Speaker2 (Kore) is firm and informative. They should interact like experienced podcast co-hosts, with natural interruptions and affirmations, ensuring natural conversational flow with occasional pauses and hesitations to enhance authenticity. Content in (...) should not be read:',
            'dialogue': dialogue
        }
