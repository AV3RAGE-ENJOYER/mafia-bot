-- +goose Up
CREATE TABLE IF NOT EXISTS public.admins (
    user_id BIGINT NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

CREATE TABLE IF NOT EXISTS public.users (
    user_id BIGINT NOT NULL,
    username text,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE public.users OWNER TO postgres;

INSERT INTO public.admins("user_id") VALUES(756278646);
INSERT INTO public.admins("user_id") VALUES(349372963);
INSERT INTO public.admins("user_id") VALUES(6516930465);

-- +goose Down
DROP TABLE public.admins;
DROP TABLE public.users;