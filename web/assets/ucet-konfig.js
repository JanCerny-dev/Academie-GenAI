/* Konfigurace Firebase pro přihlášení Google účtem (assets/ucet.js).
   Hodnoty jsou z Firebase konzole: Project settings → Your apps → Web app → firebaseConfig.
   Nejsou tajné: identifikují projekt, data chrání pravidla Firestore (firebase/firestore.rules).
   Dokud je tu null, přihlášení se na webu nezobrazí a vše běží jen v prohlížeči. */
window.GENAI_FIREBASE = {
  apiKey: "AIzaSyBHzRL2BunaE2TA5b61PQ51tK3INkOxA-0",
  authDomain: "azik-academy.firebaseapp.com",
  projectId: "azik-academy",
  appId: "1:1097154729456:web:128347d95f11f7352eb935"
};
