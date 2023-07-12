\connect railway

CREATE TABLE public.results (
    date date DEFAULT CURRENT_DATE NOT NULL,
    responses text
);

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_pkey PRIMARY KEY (date);

ALTER TABLE public.results OWNER TO postgres;

CREATE TABLE public.users (
    id SERIAL NOT NULL,
    token text NOT NULL,
    max_streak int DEFAULT 0,
    current_streak int DEFAULT 0,
    total_solves int DEFAULT 0,
    last_solve date DEFAULT CURRENT_DATE - INTEGER '1' NOT NULL
);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_token_key UNIQUE (token);

ALTER TABLE public.users OWNER TO postgres;