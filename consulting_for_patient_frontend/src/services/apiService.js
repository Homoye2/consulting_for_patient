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

// Méthodes contraceptives
export const methodesService = {
  getAll: (params) => api.get('/methodes-contraceptives/', { params }),
  getById: (id) => api.get(`/methodes-contraceptives/${id}/`),
  create: (data) => api.post('/methodes-contraceptives/', data),
  update: (id, data) => api.put(`/methodes-contraceptives/${id}/`, data),
  delete: (id) => api.delete(`/methodes-contraceptives/${id}/`),
}

// Stocks
export const stocksService = {
  getAll: (params) => api.get('/stocks/', { params }),
  getById: (id) => api.get(`/stocks/${id}/`),
  create: (data) => api.post('/stocks/', data),
  update: (id, data) => api.put(`/stocks/${id}/`, data),
  delete: (id) => api.delete(`/stocks/${id}/`),
  getAlertes: () => api.get('/stocks/alertes/'),
  getRuptures: () => api.get('/stocks/ruptures/'),
}

// Prescriptions
export const prescriptionsService = {
  getAll: (params) => api.get('/prescriptions/', { params }),
  getById: (id) => api.get(`/prescriptions/${id}/`),
  create: (data) => api.post('/prescriptions/', data),
  update: (id, data) => api.put(`/prescriptions/${id}/`, data),
  delete: (id) => api.delete(`/prescriptions/${id}/`),
}

// Mouvements de stock
export const mouvementsService = {
  getAll: (params) => api.get('/mouvements-stock/', { params }),
  getById: (id) => api.get(`/mouvements-stock/${id}/`),
  create: (data) => api.post('/mouvements-stock/', data),
}

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
  getById: (id) => api.get(`/services/${id}/`),
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

