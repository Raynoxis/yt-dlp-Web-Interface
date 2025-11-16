# 📖 Guide d'utilisation

## Interface principale

### 1. Analyser une vidéo

1. Collez l'URL YouTube dans le champ de saisie
2. Cliquez sur "🔍 Analyser la vidéo"
3. Attendez quelques secondes

L'application va récupérer :
- Le titre de la vidéo
- La miniature
- Tous les formats disponibles (vidéo et audio)

### 2. Sélectionner les formats

#### Format vidéo
- Choisissez la résolution souhaitée (1080p, 720p, etc.)
- Ou laissez "Meilleure qualité auto"

#### Format audio
- Sélectionnez la qualité audio
- Ou laissez "Meilleure qualité auto"

### 3. Options de sortie

#### Conteneur
- **MP4** : Compatible universellement (recommandé)
- **MKV** : Meilleure qualité, fichiers plus gros
- **WebM** : Format web, plus léger

#### Codec Audio
- **AAC** : Standard, excellente qualité (recommandé)
- **MP3** : Compatible partout
- **Opus** : Meilleure qualité/taille
- **Copy** : Conserve l'audio original (pas de réencodage)

#### Bitrate Audio
- **128 kbps** : Qualité correcte, fichier léger
- **192 kbps** : Bon compromis (recommandé)
- **256 kbps** : Très bonne qualité
- **320 kbps** : Qualité maximale

> ⚠️ Le bitrate est désactivé si vous sélectionnez "Copy"

### 4. Télécharger

1. Cliquez sur "⬇️ Télécharger"
2. Attendez la fin du traitement
3. Consultez la commande exécutée
4. Cliquez sur "💾 Télécharger le fichier"

## Exemples d'utilisation

### Qualité maximale MP4

1. Sélectionnez le format vidéo le plus élevé (ex: 1080p60)
2. Sélectionnez le format audio le plus élevé
3. Conteneur : MP4
4. Codec : AAC
5. Bitrate : 320k

### Audio seulement

1. Ne sélectionnez pas de format vidéo
2. Sélectionnez le meilleur format audio
3. Codec : MP3 ou AAC
4. Bitrate : 320k

### Copie directe (rapide)

1. Sélectionnez vos formats
2. Codec : Copy
3. Le téléchargement sera plus rapide (pas de réencodage)

## Commandes équivalentes

L'interface affiche la commande yt-dlp exécutée. Exemples :

### Qualité max avec AAC
```bash
yt-dlp -f "137+140" --merge-output-format mp4 --postprocessor-args "ffmpeg:-c:a aac -b:a 192k" "URL"
```

### Copy direct
```bash
yt-dlp -f "137+140" --merge-output-format mp4 "URL"
```

## Astuces

### Téléchargement rapide
- Utilisez "Copy" si les formats natifs vous conviennent
- Évitez le réencodage audio

### Meilleure qualité
- Sélectionnez manuellement les meilleurs formats
- Utilisez AAC 320k
- Préférez MKV pour la qualité maximale

### Compatibilité maximale
- Utilisez MP4 + AAC 192k
- Fonctionne sur tous les appareils

## FAQ

**Q : Pourquoi le téléchargement est long ?**
R : Le réencodage audio prend du temps. Utilisez "Copy" pour accélérer.

**Q : Le bitrate est grisé, pourquoi ?**
R : Vous avez sélectionné "Copy", le bitrate ne peut pas être modifié sans réencodage.

**Q : Puis-je télécharger plusieurs vidéos ?**
R : Oui, mais une à la fois. Les anciens fichiers sont automatiquement supprimés.

**Q : Où sont stockés les fichiers ?**
R : Dans le conteneur à `/app/downloads`. Configurez un volume pour les conserver.

## Limites

- Vidéos publiques YouTube uniquement
- Timeout à 10 minutes par téléchargement
- Un téléchargement à la fois
