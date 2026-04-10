import streamlit as st
import requests
from deep_translator import GoogleTranslator
import zlib, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# �� PUT YOUR OPENROUTER API KEY HERE
OPENROUTER_API_KEY = &quot;sk-or-v1-
ff0394f99fadc05c93c52d3711afd71855d6827231f341bdc0c8ec9851a68722&quot;
BACKEND_URL = &quot;http://127.0.0.1:8000/send&quot;
# �� Languages (UPDATED)
LANG = {
    &quot;English&quot;:&quot;en&quot;,
    &quot;Hindi&quot;:&quot;hi&quot;,
    &quot;Kannada&quot;:&quot;kn&quot;,
    &quot;Tamil&quot;:&quot;ta&quot;,
    &quot;Telugu&quot;:&quot;te&quot;,
    &quot;Malayalam&quot;:&quot;ml&quot;
}
# �� Emoji map (UPDATED)
EMOJI = {
    &quot;joy&quot;:&quot;��&quot;,
    &quot;sadness&quot;:&quot;��&quot;,
    &quot;anger&quot;:&quot;��&quot;,
    &quot;fear&quot;:&quot;��&quot;,
    &quot;surprise&quot;:&quot;��&quot;,
    &quot;confusion&quot;:&quot;��&quot;,
    &quot;neutral&quot;:&quot;��&quot;
}
# �� SMART EMOTION DETECTION (LLM)
def detect_emotion(text):
    url = &quot;https://openrouter.ai/api/v1/chat/completions&quot;
    headers = {
        &quot;Authorization&quot;: f&quot;Bearer {OPENROUTER_API_KEY}&quot;,
        &quot;Content-Type&quot;: &quot;application/json&quot;
    }
    prompt = f&quot;&quot;&quot;
    Identify the emotion of this sentence.
    Only return ONE word from:
    joy, sadness, anger, fear, surprise, confusion, neutral.
    Sentence: &quot;{text}&quot;
    &quot;&quot;&quot;
    data = {
        &quot;model&quot;: &quot;openai/gpt-3.5-turbo&quot;,

        &quot;messages&quot;: [{&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: prompt}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        emotion = result[&quot;choices&quot;][0][&quot;message&quot;][&quot;content&quot;].strip().lower()
        return emotion
    except:
        return &quot;neutral&quot;
# �� Encryption
def encrypt(data):
    key = AESGCM.generate_key(bit_length=128)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, data, None)
    return encrypted, key, nonce
# UI
st.title(&quot;�� CrypTalk Sender&quot;)
sender = st.text_input(&quot;Sender&quot;)
receiver = st.text_input(&quot;Receiver&quot;)
s_lang = st.selectbox(&quot;Sender Language&quot;, list(LANG.keys()))
r_lang = st.selectbox(&quot;Receiver Language&quot;, list(LANG.keys()))
msg = st.text_area(&quot;Message&quot;)
if st.button(&quot;Send&quot;):
    if not msg.strip():
        st.warning(&quot;Enter message&quot;)
    else:
        translated = GoogleTranslator(
            source=LANG[s_lang],
            target=&quot;en&quot;
        ).translate(msg)
        # �� Emotion detection
        emotion = detect_emotion(translated)
        emoji = EMOJI.get(emotion, &quot;��&quot;)
        tagged = f&quot;[{emotion.upper()} {emoji}] {translated}&quot;
        compressed = zlib.compress(tagged.encode())
        enc, key, nonce = encrypt(compressed)
        payload = {
            &quot;sender&quot;: sender,
            &quot;receiver&quot;: receiver,
            &quot;sender_lang&quot;: s_lang,
            &quot;receiver_lang&quot;: r_lang,
            &quot;emotion&quot;: emotion,

            &quot;encrypted&quot;: enc.hex(),
            &quot;key&quot;: key.hex(),
            &quot;nonce&quot;: nonce.hex(),
            &quot;tagged_text&quot;: tagged
        }
        res = requests.post(BACKEND_URL, json=payload)
        if res.status_code == 200:
            st.success(&quot;✅ Message Sent&quot;)
            st.write(tagged)
        else:
            st.error(&quot;Error sending&quot;)
