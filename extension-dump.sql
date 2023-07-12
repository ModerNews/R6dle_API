\connect railway

CREATE TABLE public.results (
    date date DEFAULT CURRENT_DATE NOT NULL,
    responses text
);

ALTER TABLE ONLY public.results
    ADD CONSTRAINT results_pkey PRIMARY KEY (date);

ALTER TABLE public.results OWNER TO postgres;