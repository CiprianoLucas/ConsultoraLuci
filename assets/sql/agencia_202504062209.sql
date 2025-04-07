CREATE TABLE public.feedback (
	id int4 NOT NULL,
	colaborador int4 NOT NULL,
	cooperado int4 NOT NULL,
	descricao text NOT NULL,
	CONSTRAINT feedback_pk PRIMARY KEY (id),
	CONSTRAINT feedback_colaborador_fk FOREIGN KEY (colaborador) REFERENCES public.colaborador(id),
	CONSTRAINT feedback_cooperado_fk FOREIGN KEY (cooperado) REFERENCES public.cooperado(id)
);

INSERT INTO public.agencia (id,cep,senha) VALUES
	 (1,'89045200','$2b$12$sinBlwUoVe976oXpaNaix.HDREcNhIqYkqHC.Qd9MP4unr6S9kc0O'),
	 (2,'89050800','$2b$12$sinBlwUoVe976oXpaNaix.HDREcNhIqYkqHC.Qd9MP4unr6S9kc0O'),
	 (3,'89056100','$2b$12$sinBlwUoVe976oXpaNaix.HDREcNhIqYkqHC.Qd9MP4unr6S9kc0O');
