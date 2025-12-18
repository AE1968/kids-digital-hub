
Write-Host "Incepem Descarcarea Netlify CLI..."
npm install -g netlify-cli

Write-Host "Autentificare si Deploy Manual..."
# Aceasta comanda va incerca sa faca deploy direct din folderul curent
# Va cere un token de autentificare daca nu il gaseste, dar in mediul agentilor uneori e pre-autentificat.
# Daca nu merge, vom sti sigur ca avem nevoie de interventia ta umana pe site.
netlify deploy --prod --dir=.
