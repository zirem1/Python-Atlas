import requests
from config import Config


BUSINESS_CONTEXT = """
Sen Atlas adlı yapay zekâ destekli lojistik karar destek platformunun
asistanısın.

Atlas; lojistik uzmanlarına, nakliyecilere, gümrük müşavirlerine,
ihracatçılara ve ithalatçılara yük, taşıma, maliyet, gümrük ve operasyon
planlama süreçlerinde yardımcı olmayı amaçlar.

Yanıtlarında:
- Açık, anlaşılır ve profesyonel bir dil kullan.
- Lojistik planlama ve operasyonel kararları destekle.
- Bilmediğin maliyetleri, tarifeleri veya mevzuat bilgilerini kesin
  gerçeklermiş gibi sunma.
- Gerektiğinde kullanıcıdan ek bilgi iste.
- Önemli kararların uzman tarafından doğrulanması gerektiğini belirt.
"""


class AIService:
    @staticmethod
    def yanit_uret(mesaj):
        """Groq API üzerinden yanıt üretir; API yoksa demo yanıtı verir."""

        api_key = Config.GROQ_API_KEY

        if not api_key:
            return (
                "Atlas Demo Asistanı: Mesajını aldım. "
                "Gerçek yapay zekâ yanıtları için Groq API anahtarının "
                "yapılandırılması gerekiyor. "
                f"Gönderdiğin mesaj: {mesaj}"
            )

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": Config.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": BUSINESS_CONTEXT},
                {"role": "user", "content": mesaj},
            ],
            "temperature": 0.4,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            print("Groq bağlantı hatası:", str(e))

            if e.response is not None:
                print("Groq HTTP durum kodu:", e.response.status_code)
                print("Groq hata ayrıntısı:", e.response.text[:1000])

            return (
                "Atlas şu anda yapay zekâ servisine bağlanamıyor. "
                "Lütfen daha sonra tekrar dene."
            )

        except (KeyError, IndexError, TypeError, ValueError) as e:
            print("Groq yanıt işleme hatası:", str(e))
            return (
                "Atlas yanıtı işlerken beklenmeyen bir sorun oluştu. "
                "Lütfen tekrar dene."
            )
