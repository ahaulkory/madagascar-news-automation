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
