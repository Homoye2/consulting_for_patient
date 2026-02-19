erDiagram
    User ||--o| Patient : "has profile"
    User ||--o{ RendezVous : "creates"
    User ||--o{ ConsultationPF : "performs"
    User ||--o{ Pharmacie : "owns"
    
    Patient ||--o{ RendezVous : "has"
    Patient ||--o{ ConsultationPF : "has"
    Patient ||--o{ ContactMessage : "sends"
    
    Pharmacie ||--o{ StockProduit : "has stocks"
    
    LandingPageContent ||--o{ Service : "has"
    LandingPageContent ||--o{ Value : "has"
    
    User {
        bigint id PK
        string nom
        string email UK
        string role
        boolean actif
        boolean is_staff
        boolean is_superuser
        datetime date_joined
        datetime last_login
    }
    
    Pharmacie {
        bigint id PK
        string nom
        text adresse
        string telephone
        string email
        bigint user_id FK
        boolean actif
        datetime created_at
        datetime updated_at
    }
    
    Patient {
        bigint id PK
        string nom
        string prenom
        date dob
        string sexe
        string telephone
        string email UK
        text adresse
        text antecedents
        text allergies
        bigint user_id FK
        datetime created_at
        datetime updated_at
    }
    
    RendezVous {
        bigint id PK
        bigint patient_id FK
        bigint user_id FK
        datetime datetime
        string statut
        text notes
        datetime created_at
        datetime updated_at
    }
    
    ConsultationPF {
        bigint id PK
        bigint patient_id FK
        bigint user_id FK
        datetime date
        text anamnese
        text examen
        boolean methode_posee
        text effets_secondaires
        text notes
        text observation
        datetime created_at
        datetime updated_at
    }
    
    LandingPageContent {
        bigint id PK
        string logo_text
        string hero_title
        text hero_description
        string hero_button_primary
        string hero_button_secondary
        string about_title
        text about_description_1
        text about_description_2
        string about_stat_1_value
        string about_stat_1_label
        string about_stat_2_value
        string about_stat_2_label
        string services_title
        text services_subtitle
        string values_title
        text values_subtitle
        text footer_about_text
        string footer_address
        string footer_phone
        string footer_email
        string footer_facebook
        string footer_twitter
        string footer_instagram
        string footer_linkedin
        datetime created_at
        datetime updated_at
    }
    
    Service {
        bigint id PK
        bigint landing_page_id FK
        string titre
        text description
        text contenu_detail
        string icone
        int ordre
    }
    
    Value {
        bigint id PK
        bigint landing_page_id FK
        string titre
        text description
        string icone
        int ordre
    }
    
    ContactMessage {
        bigint id PK
        bigint patient_id FK
        string nom
        string email
        string sujet
        text message
        boolean lu
        datetime date_creation
    }

