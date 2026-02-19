# Guide de déploiement des applications frontend

## Builds générés avec succès ✅

Les trois applications React/Vite ont été compilées pour la production:

### 1. e-sora (Application principale - Super Admin)
- **Chemin du build**: `e-sora/dist/`
- **Taille**: ~1.4 MB (JS) + 40 KB (CSS)
- **URL de déploiement suggérée**: `https://e-sora.onglalumiere.org/`

### 2. e-sora-hopital (Application Hôpital)
- **Chemin du build**: `e-sora-hopital/dist/`
- **Taille**: ~650 KB (JS total) + 35 KB (CSS)
- **URL de déploiement suggérée**: `https://hopital.e-sora.onglalumiere.org/`

### 3. e-sora-pharmacie (Application Pharmacie)
- **Chemin du build**: `e-sora-pharmacie/dist/`
- **Taille**: ~610 KB (JS total) + 41 KB (CSS)
- **URL de déploiement suggérée**: `https://pharmacie.e-sora.onglalumiere.org/`

---

## Structure des fichiers de build

Chaque dossier `dist/` contient:
```
dist/
├── index.html              # Point d'entrée HTML
├── assets/
│   ├── *.js               # Fichiers JavaScript compilés
│   ├── *.css              # Fichiers CSS compilés
│   └── *.png/jpg          # Images et assets
└── vite.svg               # Favicon (optionnel)
```

---

## Option 1: Déploiement sur cPanel (Recommandé)

### Étape 1: Préparer les fichiers

Sur votre machine locale:

```bash
# Compresser chaque build
cd e-sora
tar -czf e-sora-build.tar.gz dist/

cd ../e-sora-hopital
tar -czf e-sora-hopital-build.tar.gz dist/

cd ../e-sora-pharmacie
tar -czf e-sora-pharmacie-build.tar.gz dist/
```

### Étape 2: Créer les sous-domaines dans cPanel

1. Connectez-vous à **cPanel**
2. Allez dans **Domains** ou **Subdomains**
3. Créez les sous-domaines:
   - `hopital.e-sora.onglalumiere.org` → Document Root: `/home/onglsmjm/hopital.e-sora.onglalumiere.org`
   - `pharmacie.e-sora.onglalumiere.org` → Document Root: `/home/onglsmjm/pharmacie.e-sora.onglalumiere.org`

### Étape 3: Uploader les fichiers

#### Via FTP/SFTP (FileZilla):

1. Connectez-vous via SFTP
2. Pour chaque application:
   - Uploadez le contenu du dossier `dist/` dans le Document Root correspondant
   - **e-sora**: `/home/onglsmjm/e_sora.onglalumiere.org/` (ou créer un sous-dossier `app/`)
   - **e-sora-hopital**: `/home/onglsmjm/hopital.e-sora.onglalumiere.org/`
   - **e-sora-pharmacie**: `/home/onglsmjm/pharmacie.e-sora.onglalumiere.org/`

#### Via SSH:

```bash
# Se connecter au serveur
ssh onglsmjm@server305.com

# Créer les répertoires
mkdir -p ~/hopital.e-sora.onglalumiere.org
mkdir -p ~/pharmacie.e-sora.onglalumiere.org

# Uploader les archives (depuis votre machine locale)
scp e-sora/e-sora-build.tar.gz onglsmjm@server305.com:~/
scp e-sora-hopital/e-sora-hopital-build.tar.gz onglsmjm@server305.com:~/
scp e-sora-pharmacie/e-sora-pharmacie-build.tar.gz onglsmjm@server305.com:~/

# Sur le serveur, extraire les fichiers
cd ~/e_sora.onglalumiere.org/
tar -xzf ~/e-sora-build.tar.gz --strip-components=1

cd ~/hopital.e-sora.onglalumiere.org/
tar -xzf ~/e-sora-hopital-build.tar.gz --strip-components=1

cd ~/pharmacie.e-sora.onglalumiere.org/
tar -xzf ~/e-sora-pharmacie-build.tar.gz --strip-components=1

# Nettoyer
rm ~/*.tar.gz
```

### Étape 4: Configurer les .htaccess

Pour chaque application, créez un fichier `.htaccess` pour gérer le routing SPA:

```bash
# Pour e-sora
cat > ~/e_sora.onglalumiere.org/.htaccess << 'EOF'
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
EOF

# Pour e-sora-hopital
cat > ~/hopital.e-sora.onglalumiere.org/.htaccess << 'EOF'
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
EOF

# Pour e-sora-pharmacie
cat > ~/pharmacie.e-sora.onglalumiere.org/.htaccess << 'EOF'
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
EOF
```

### Étape 5: Activer SSL (HTTPS)

1. Dans cPanel, allez dans **SSL/TLS Status**
2. Sélectionnez tous les domaines:
   - `e-sora.onglalumiere.org`
   - `hopital.e-sora.onglalumiere.org`
   - `pharmacie.e-sora.onglalumiere.org`
3. Cliquez sur **Run AutoSSL** (Let's Encrypt gratuit)

### Étape 6: Tester les applications

Visitez:
- `https://e-sora.onglalumiere.org/`
- `https://hopital.e-sora.onglalumiere.org/`
- `https://pharmacie.e-sora.onglalumiere.org/`

---

## Option 2: Déploiement sur Vercel (Alternative)

### Avantages:
- Déploiement automatique depuis Git
- SSL gratuit
- CDN global
- Domaines personnalisés gratuits

### Étapes:

1. **Créer un compte Vercel**: https://vercel.com
2. **Connecter votre repository GitHub**
3. **Importer les projets**:
   - e-sora
   - e-sora-hopital
   - e-sora-pharmacie
4. **Configuration de build** (Vercel détecte automatiquement Vite):
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. **Configurer les domaines personnalisés**:
   - e-sora → `e-sora.onglalumiere.org`
   - e-sora-hopital → `hopital.e-sora.onglalumiere.org`
   - e-sora-pharmacie → `pharmacie.e-sora.onglalumiere.org`

---

## Option 3: Déploiement sur Netlify (Alternative)

### Avantages:
- Interface simple
- Déploiement par drag & drop
- SSL gratuit
- Formulaires et fonctions serverless

### Étapes:

1. **Créer un compte Netlify**: https://netlify.com
2. **Déployer par drag & drop**:
   - Glissez le dossier `dist/` de chaque application
3. **Ou connecter Git** pour déploiement automatique
4. **Configurer les domaines personnalisés**

---

## Configuration des variables d'environnement

### Important: URL de l'API

Chaque application doit pointer vers votre backend Django.

#### e-sora

Créez `e-sora/.env.production`:
```env
VITE_API_URL=https://e-sora.onglalumiere.org/api
```

#### e-sora-hopital

Créez `e-sora-hopital/.env.production`:
```env
VITE_API_URL=https://e-sora.onglalumiere.org/api
```

#### e-sora-pharmacie

Créez `e-sora-pharmacie/.env.production`:
```env
VITE_API_URL=https://e-sora.onglalumiere.org/api
```

**Puis rebuild:**
```bash
npm run build
```

---

## Mise à jour des applications

### Méthode 1: Rebuild et re-upload

```bash
# Local
cd e-sora
npm run build

# Upload via SFTP ou:
scp -r dist/* onglsmjm@server305.com:~/e_sora.onglalumiere.org/
```

### Méthode 2: Script de déploiement automatique

Créez `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Déploiement des applications frontend"

# Build
echo "📦 Build e-sora..."
cd e-sora && npm run build && cd ..

echo "📦 Build e-sora-hopital..."
cd e-sora-hopital && npm run build && cd ..

echo "📦 Build e-sora-pharmacie..."
cd e-sora-pharmacie && npm run build && cd ..

# Upload
echo "⬆️  Upload vers le serveur..."
scp -r e-sora/dist/* onglsmjm@server305.com:~/e_sora.onglalumiere.org/
scp -r e-sora-hopital/dist/* onglsmjm@server305.com:~/hopital.e-sora.onglalumiere.org/
scp -r e-sora-pharmacie/dist/* onglsmjm@server305.com:~/pharmacie.e-sora.onglalumiere.org/

echo "✅ Déploiement terminé!"
```

Utilisation:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Optimisations recommandées

### 1. Compression Gzip

Ajoutez dans `.htaccess`:

```apache
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>
```

### 2. Cache des assets

```apache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

### 3. Sécurité

```apache
# Empêcher l'accès aux fichiers sensibles
<FilesMatch "\.(env|json|lock)$">
  Require all denied
</FilesMatch>

# Headers de sécurité
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set X-XSS-Protection "1; mode=block"
</IfModule>
```

---

## Checklist de déploiement

### e-sora (Application principale)
- [ ] Build généré (`npm run build`)
- [ ] Fichiers uploadés sur le serveur
- [ ] `.htaccess` configuré pour SPA routing
- [ ] SSL activé (HTTPS)
- [ ] URL de l'API configurée
- [ ] Application accessible et fonctionnelle

### e-sora-hopital
- [ ] Build généré
- [ ] Sous-domaine créé (`hopital.e-sora.onglalumiere.org`)
- [ ] Fichiers uploadés
- [ ] `.htaccess` configuré
- [ ] SSL activé
- [ ] URL de l'API configurée
- [ ] Application accessible

### e-sora-pharmacie
- [ ] Build généré
- [ ] Sous-domaine créé (`pharmacie.e-sora.onglalumiere.org`)
- [ ] Fichiers uploadés
- [ ] `.htaccess` configuré
- [ ] SSL activé
- [ ] URL de l'API configurée
- [ ] Application accessible

---

## Dépannage

### Erreur 404 sur les routes

**Problème**: Les routes React ne fonctionnent pas (404 sur refresh).

**Solution**: Vérifiez que le `.htaccess` est présent et correct.

### Assets ne se chargent pas

**Problème**: CSS/JS ne se charge pas.

**Solution**: Vérifiez les permissions:
```bash
chmod -R 755 ~/e_sora.onglalumiere.org/assets/
```

### Erreur CORS

**Problème**: L'application ne peut pas communiquer avec l'API.

**Solution**: Vérifiez `CORS_ALLOWED_ORIGINS` dans le backend Django.

---

## Support

Pour toute question sur le déploiement:
1. Vérifiez les logs du navigateur (Console)
2. Vérifiez les logs Apache sur le serveur
3. Testez l'API backend séparément

---

**Builds générés le**: 19 février 2026
**Versions**:
- e-sora: Vite 7.2.2
- e-sora-hopital: Vite 7.2.5
- e-sora-pharmacie: Vite 7.3.0
