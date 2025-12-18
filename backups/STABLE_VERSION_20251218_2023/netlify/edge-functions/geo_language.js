
// 🌍 NETLIFY EDGE FUNCTION: Geo-Language Detection
// Detectează țara vizitatorului și setează automat limba potrivită.
// Rulează direct pe serverele Netlify (Edge Network) pentru viteză maximă.

export default async (request, context) => {
    // Obține țara din contextul Netlify (GeoIP)
    const countryCode = context.geo?.country?.code || "US";

    // Mapare Țară -> Limbă
    const countryToLang = {
        "RO": "ro", // România -> Română
        "MD": "ro", // Moldova -> Română
        "FR": "fr", // Franța -> Franceză
        "BE": "fr", // Belgia -> Franceză
        "DE": "de", // Germania -> Germană
        "AT": "de", // Austria -> Germană
        "ES": "es", // Spania -> Spaniolă
        "MX": "es", // Mexic -> Spaniolă
        "CN": "zh", // China -> Chineză
        "JP": "ja", // Japonia -> Japoneză
        "KR": "ko", // Coreea -> Coreeană
        "GB": "en", // UK -> Engleză
        "US": "en"  // SUA -> Engleză
    };

    // Determină limba (default: engleză)
    const lang = countryToLang[countryCode] || "en";

    // Verifică dacă utilizatorul a setat deja o limbă manual (cookie)
    const cookies = request.headers.get("cookie");
    if (cookies && cookies.includes("nf_lang")) {
        // Dacă utilizatorul a ales deja, respectăm alegerea lui și nu facem nimic
        return context.next();
    }

    // Dacă e prima vizită, injectăm un script mic care va seta limba în aplicație
    // Sau, mai elegant, setăm un cookie și lăsăm JS-ul din frontend să citească.

    const response = await context.next();
    response.headers.set("Set-Cookie", `nf_lang=${lang}; Path=/; SameSite=Lax`);

    return response;
};
