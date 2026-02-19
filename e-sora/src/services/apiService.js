import api from '../lib/api'

// Patients
export const patientsService = {
  getAll: (params) => api.get('/patients/', { params }),
  getById: (id) => api.get(`/patients/${id}/`),
  create: (data) => api.post('/patients/', data),
  update: (id, data) => api.put(`/patients/${id}/`, data),
  delete: (id) => api.delete(`/patients/${id}/`),
  getConsultations: (id) => api.get(`/patients/${id}/consultations/`),
  getRendezVous: (id) => api.get(`/patients/${id}/rendez_vous/`),
}

// Consultations
export const consultationsService = {
  getAll: (params) => api.get('/consultations/', { params }),
  getById: (id) => api.get(`/consultations/${id}/`),
  create: (data) => api.post('/consultations/', data),
  update: (id, data) => api.put(`/consultations/${id}/`, data),
  delete: (id) => api.delete(`/consultations/${id}/`),
  getPrescriptions: (id) => api.get(`/consultations/${id}/prescriptions/`),
}

// Rendez-vous
export const rendezVousService = {
  getAll: (params) => api.get('/rendez-vous/', { params }),
  getById: (id) => api.get(`/rendez-vous/${id}/`),
  create: (data) => api.post('/rendez-vous/', data),
  update: (id, data) => api.put(`/rendez-vous/${id}/`, data),
  delete: (id) => api.delete(`/rendez-vous/${id}/`),
  getAgenda: (params) => api.get('/rendez-vous/agenda/', { params }),
  confirmer: (id) => api.post(`/rendez-vous/${id}/confirmer/`),
  annuler: (id) => api.post(`/rendez-vous/${id}/annuler/`),
}

// Stocks
export const stocksService = {
  getAll: (params) => api.get('/stocks-produits/', { params }),
  getById: (id) => api.get(`/stocks-produits/${id}/`),
  create: (data) => api.post('/stocks-produits/', data),
  update: (id, data) => api.put(`/stocks-produits/${id}/`, data),
  delete: (id) => api.delete(`/stocks-produits/${id}/`),
  getAlertes: () => api.get('/stocks-produits/alertes/'),
  getExpirations: () => api.get('/stocks-produits/expirations/'),
}

// Mouvements de stock - Fonctionnalité supprimée
// export const mouvementsService = {
//   getAll: (params) => api.get('/mouvements-stock/', { params }),
//   getById: (id) => api.get(`/mouvements-stock/${id}/`),
//   create: (data) => api.post('/mouvements-stock/', data),
// }

// Prescriptions - Fonctionnalité supprimée
// export const prescriptionsService = {
//   getAll: (params) => api.get('/prescriptions/', { params }),
//   getById: (id) => api.get(`/prescriptions/${id}/`),
//   create: (data) => api.post('/prescriptions/', data),
//   update: (id, data) => api.put(`/prescriptions/${id}/`, data),
//   delete: (id) => api.delete(`/prescriptions/${id}/`),
// }

// Utilisateurs
export const usersService = {
  getAll: (params) => api.get('/users/', { params }),
  getById: (id) => api.get(`/users/${id}/`),
  getMe: () => api.get('/users/me/'),
  create: (data) => api.post('/users/', data),
  update: (id, data) => api.put(`/users/${id}/`, data),
  delete: (id) => api.delete(`/users/${id}/`),
  activate: (id) => api.post(`/users/${id}/activate/`),
  deactivate: (id) => api.post(`/users/${id}/deactivate/`),
}

// Statistiques
export const statistiquesService = {
  getGeneral: () => api.get('/statistiques/'),
  getConsultations: (params) => api.get('/statistiques/consultations/', { params }),
  getRendezVous: (params) => api.get('/statistiques/rendez-vous/', { params }),
  getStocks: () => api.get('/statistiques/stocks/'),
}

// Analytics
export const analyticsService = {
  getDashboard: () => api.get('/analytics/dashboard/'),
}

// Admin Dashboard
export const adminService = {
  getSystemHealth: () => api.get('/admin/system-health/'),
  getRecentActivity: (params) => api.get('/admin/recent-activity/', { params }),
  getSystemAlerts: () => api.get('/admin/system-alerts/'),
  getSecurityStats: () => api.get('/admin/security-stats/'),
  getSecurityAlerts: () => api.get('/admin/security-alerts/'),
  getLoginAttempts: (params) => api.get('/admin/login-attempts/', { params }),
  broadcastNotification: (data) => api.post('/admin/broadcast-notification/', data),
}

// Fournisseurs
export const fournisseursService = {
  getAll: (params) => api.get('/fournisseurs/', { params }),
  getById: (id) => api.get(`/fournisseurs/${id}/`),
  create: (data) => api.post('/fournisseurs/', data),
  update: (id, data) => api.put(`/fournisseurs/${id}/`, data),
  partialUpdate: (id, data) => api.patch(`/fournisseurs/${id}/`, data),
  delete: (id) => api.delete(`/fournisseurs/${id}/`),
  activer: (id) => api.post(`/fournisseurs/${id}/activer/`),
  desactiver: (id) => api.post(`/fournisseurs/${id}/desactiver/`),
  creerCompte: (id) => api.post(`/fournisseurs/${id}/creer-compte/`),
}

// Landing Page
export const landingPageService = {
  getPublic: () => api.get('/landing-page/public/'),
  get: () => api.get('/landing-page/'),
  update: (data) => api.put('/landing-page/1/', data),
  partialUpdate: (data) => api.patch('/landing-page/1/', data),
}

// Services (de la landing page)
export const landingServicesService = {
  getAll: () => api.get('/services/'),
  getById: (id) => api.get(`/services/${id}/`), // Endpoint public avec AllowAny
  getPublic: () => api.get('/services/public/'),
  create: (data) => api.post('/services/', data),
  update: (id, data) => api.put(`/services/${id}/`, data),
  delete: (id) => api.delete(`/services/${id}/`),
}

// Values (de la landing page)
export const landingValuesService = {
  getAll: () => api.get('/values/'),
  getById: (id) => api.get(`/values/${id}/`),
  create: (data) => api.post('/values/', data),
  update: (id, data) => api.put(`/values/${id}/`, data),
  delete: (id) => api.delete(`/values/${id}/`),
}

// Messages de contact
export const contactMessagesService = {
  getAll: (params) => api.get('/contact-messages/', { params }),
  getById: (id) => api.get(`/contact-messages/${id}/`),
  create: (data) => api.post('/contact-messages/', data),
}

// Hôpitaux
export const hopitauxService = {
  getAll: (params) => api.get('/hopitaux/', { params }),
  getById: (id) => api.get(`/hopitaux/${id}/`),
  create: (data) => api.post('/hopitaux/', data),
  update: (id, data) => api.put(`/hopitaux/${id}/`, data),
  delete: (id) => api.delete(`/hopitaux/${id}/`),
  resetAdminPassword: (id) => api.post(`/hopitaux/${id}/reset_admin_password/`),
  suspendre: (id) => api.post(`/hopitaux/${id}/suspendre/`),
  activer: (id) => api.post(`/hopitaux/${id}/activer/`),
}

// Pharmacies
export const pharmaciesService = {
  getAll: (params) => api.get('/pharmacies/', { params }),
  getById: (id) => api.get(`/pharmacies/${id}/`),
  create: (data) => api.post('/pharmacies/', data),
  update: (id, data) => api.put(`/pharmacies/${id}/`, data),
  delete: (id) => api.delete(`/pharmacies/${id}/`),
  activer: (id) => api.post(`/pharmacies/${id}/activer/`),
  suspendre: (id) => api.post(`/pharmacies/${id}/suspendre/`),
  resetAdminPassword: (id) => api.post(`/pharmacies/${id}/reset_admin_password/`),
}

// Spécialistes
export const specialistesService = {
  getAll: (params) => api.get('/specialistes/', { params }),
  getById: (id) => api.get(`/specialistes/${id}/`),
  create: (data) => api.post('/specialistes/', data),
  update: (id, data) => api.put(`/specialistes/${id}/`, data),
  delete: (id) => api.delete(`/specialistes/${id}/`),
}

// Commandes
export const commandesService = {
  getAll: (params) => api.get('/commandes/', { params }),
  getById: (id) => api.get(`/commandes/${id}/`),
  create: (data) => api.post('/commandes/', data),
  update: (id, data) => api.put(`/commandes/${id}/`, data),
  delete: (id) => api.delete(`/commandes/${id}/`),
}

// Produits
export const produitsService = {
  getAll: (params) => api.get('/produits/', { params }),
  getById: (id) => api.get(`/produits/${id}/`),
  create: (data) => api.post('/produits/', data),
  update: (id, data) => api.put(`/produits/${id}/`, data),
  delete: (id) => api.delete(`/produits/${id}/`),
}

