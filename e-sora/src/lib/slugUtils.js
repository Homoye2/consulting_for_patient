/**
 * Utilitaires pour la génération de slugs pour les URLs
 */

/**
 * Génère un slug à partir d'un nom et prénom
 * @param {string} nom - Nom de famille
 * @param {string} prenom - Prénom
 * @returns {string} - Slug formaté (ex: "jean-dupont")
 */
export const generatePatientSlug = (nom, prenom) => {
  if (!nom || !prenom) return ''
  
  const cleanText = (text) => {
    return text
      .toLowerCase()
      .normalize('NFD') // Décompose les caractères accentués
      .replace(/[\u0300-\u036f]/g, '') // Supprime les accents
      .replace(/[^a-z0-9\s-]/g, '') // Garde seulement lettres, chiffres, espaces et tirets
      .replace(/\s+/g, '-') // Remplace les espaces par des tirets
      .replace(/-+/g, '-') // Évite les tirets multiples
      .trim()
  }
  
  return `${cleanText(prenom)}-${cleanText(nom)}`
}

/**
 * Génère un slug pour un rendez-vous
 * @param {string} patientNom - Nom du patient
 * @param {string} patientPrenom - Prénom du patient
 * @param {string} date - Date du rendez-vous
 * @returns {string} - Slug formaté
 */
export const generateRendezVousSlug = (patientNom, patientPrenom, date) => {
  const patientSlug = generatePatientSlug(patientNom, patientPrenom)
  if (!patientSlug || !date) return ''
  
  try {
    const dateObj = new Date(date)
    const dateSlug = dateObj.toISOString().split('T')[0] // Format YYYY-MM-DD
    return `${patientSlug}-${dateSlug}`
  } catch {
    return patientSlug
  }
}

/**
 * Génère un slug pour une consultation
 * @param {string} patientNom - Nom du patient
 * @param {string} patientPrenom - Prénom du patient
 * @param {string} date - Date de la consultation
 * @returns {string} - Slug formaté
 */
export const generateConsultationSlug = (patientNom, patientPrenom, date) => {
  return generateRendezVousSlug(patientNom, patientPrenom, date)
}

/**
 * Extrait l'ID depuis une URL avec slug
 * @param {string} idWithSlug - ID avec slug (ex: "150?jean-dupont")
 * @returns {string} - ID seul
 */
export const extractIdFromSlug = (idWithSlug) => {
  if (!idWithSlug) return ''
  return idWithSlug.split('?')[0]
}

/**
 * Génère l'URL complète avec slug
 * @param {string|number} id - ID de l'entité
 * @param {string} slug - Slug généré
 * @returns {string} - URL formatée (ex: "150?jean-dupont")
 */
export const generateUrlWithSlug = (id, slug) => {
  if (!id) return ''
  if (!slug) return id.toString()
  return `${id}?${slug}`
}