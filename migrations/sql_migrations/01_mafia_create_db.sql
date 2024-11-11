-- +goose Up
CREATE TABLE public.admins (
    user_id integer NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.users OWNER TO postgres;

INSERT INTO public.admins("user_id") VALUES(756278646);
INSERT INTO public.admins("user_id") VALUES(349372963);

-- +goose Down
DROP TABLE public.admins;
DROP TABLE public.users;