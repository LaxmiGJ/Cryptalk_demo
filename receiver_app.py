import streamlit as st
import requests
from deep_translator import GoogleTranslator
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import zlib
BACKEND_URL = &quot;http://127.0.0.1:8000/get&quot;
LANG = {
    &quot;English&quot;:&quot;en&quot;,
    &quot;Hindi&quot;:&quot;hi&quot;,
    &quot;Kannada&quot;:&quot;kn&quot;,
    &quot;Tamil&quot;:&quot;ta&quot;,
    &quot;Telugu&quot;:&quot;te&quot;,
    &quot;Malayalam&quot;:&quot;ml&quot;
}
def decrypt(enc,key,nonce):
    aes = AESGCM(bytes.fromhex(key))
    return aes.decrypt(bytes.fromhex(nonce), bytes.fromhex(enc), None)
st.title(&quot;�� CrypTalk Receiver&quot;)
# �� NEW: user can choose output language
chosen_lang = st.selectbox(&quot;Choose Output Language&quot;, list(LANG.keys()))
if st.button(&quot;Receive&quot;):
    res = requests.get(BACKEND_URL)
    data = res.json()
    dec = decrypt(data[&quot;encrypted&quot;], data[&quot;key&quot;], data[&quot;nonce&quot;])
    text = zlib.decompress(dec).decode()
    # Extract only message (remove tag)
    if &quot;] &quot; in text:

        tag, msg = text.split(&quot;] &quot;, 1)
    else:
        tag, msg = &quot;&quot;, text
    translated = GoogleTranslator(
        source=&quot;en&quot;,
        target=LANG[chosen_lang]
    ).translate(msg)
    st.write(&quot;Sender:&quot;, data[&quot;sender&quot;])
    st.write(&quot;Emotion:&quot;, data[&quot;emotion&quot;])
    st.write(&quot;Original:&quot;, text)
    st.write(&quot;Translated:&quot;, f&quot;{tag}] {translated}&quot; if tag else translated)
