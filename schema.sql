-- Esegui questo script nel SQL Editor di Supabase
-- (Dashboard → SQL Editor → New query)

create table if not exists photos (
    id              uuid primary key default gen_random_uuid(),
    object_key      text not null unique,
    public_url      text not null,
    guest_name      text not null,
    filename        text,
    file_size       bigint,
    uploaded_at     timestamptz not null default now(),
    moment          text,           -- null finché non classificato con CLIP
    confidence      numeric(6,4),   -- score CLIP [0..1]
    created_at      timestamptz not null default now()
);

-- Indici utili per la gallery
create index if not exists photos_moment_idx      on photos(moment);
create index if not exists photos_uploaded_at_idx on photos(uploaded_at desc);
create index if not exists photos_guest_idx       on photos(guest_name);

-- Row Level Security: abilita ma lascia accesso libero
-- (l'autenticazione è gestita da Streamlit con password condivisa)
alter table photos enable row level security;

create policy "Allow all" on photos
    for all using (true) with check (true);
