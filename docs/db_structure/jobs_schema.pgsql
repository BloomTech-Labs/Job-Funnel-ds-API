--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.companies (
    id integer NOT NULL,
    name text,
    description text,
    size integer,
    revenue integer
);


ALTER TABLE public.companies OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.companies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.companies_id_seq OWNER TO postgres;

--
-- Name: companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.companies_id_seq OWNED BY public.companies.id;


--
-- Name: job_listings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_listings (
    id integer NOT NULL,
    post_date_utc timestamp without time zone,
    pay_min integer,
    pay_max integer,
    pay_exact integer,
    title text,
    seniority text
);


ALTER TABLE public.job_listings OWNER TO postgres;

--
-- Name: job_listings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_listings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.job_listings_id_seq OWNER TO postgres;

--
-- Name: job_listings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_listings_id_seq OWNED BY public.job_listings.id;


--
-- Name: jobs_companies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_companies (
    id integer NOT NULL,
    job_id integer NOT NULL,
    company_id integer NOT NULL
);


ALTER TABLE public.jobs_companies OWNER TO postgres;

--
-- Name: jobs_companies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_companies_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_companies_id_seq OWNER TO postgres;

--
-- Name: jobs_companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_companies_id_seq OWNED BY public.jobs_companies.id;


--
-- Name: jobs_descriptions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_descriptions (
    id integer NOT NULL,
    job_id integer NOT NULL,
    description text
);


ALTER TABLE public.jobs_descriptions OWNER TO postgres;

--
-- Name: jobs_descriptions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_descriptions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_descriptions_id_seq OWNER TO postgres;

--
-- Name: jobs_descriptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_descriptions_id_seq OWNED BY public.jobs_descriptions.id;


--
-- Name: jobs_keyphrases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_keyphrases (
    id integer NOT NULL,
    job_id integer NOT NULL,
    keyphrase text
);


ALTER TABLE public.jobs_keyphrases OWNER TO postgres;

--
-- Name: jobs_keyphrases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_keyphrases_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_keyphrases_id_seq OWNER TO postgres;

--
-- Name: jobs_keyphrases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_keyphrases_id_seq OWNED BY public.jobs_keyphrases.id;


--
-- Name: jobs_keywords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_keywords (
    id integer NOT NULL,
    job_id integer NOT NULL,
    keyword text
);


ALTER TABLE public.jobs_keywords OWNER TO postgres;

--
-- Name: jobs_keywords_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_keywords_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_keywords_id_seq OWNER TO postgres;

--
-- Name: jobs_keywords_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_keywords_id_seq OWNED BY public.jobs_keywords.id;


--
-- Name: jobs_locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.jobs_locations (
    id integer NOT NULL,
    job_id integer NOT NULL,
    location_id integer NOT NULL
);


ALTER TABLE public.jobs_locations OWNER TO postgres;

--
-- Name: jobs_locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.jobs_locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_locations_id_seq OWNER TO postgres;

--
-- Name: jobs_locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.jobs_locations_id_seq OWNED BY public.jobs_locations.id;


--
-- Name: locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.locations (
    id integer NOT NULL,
    city text,
    state_province text,
    country text
);


ALTER TABLE public.locations OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.locations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.locations_id_seq OWNER TO postgres;

--
-- Name: locations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.locations_id_seq OWNED BY public.locations.id;


--
-- Name: companies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies ALTER COLUMN id SET DEFAULT nextval('public.companies_id_seq'::regclass);


--
-- Name: job_listings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_listings ALTER COLUMN id SET DEFAULT nextval('public.job_listings_id_seq'::regclass);


--
-- Name: jobs_companies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_companies ALTER COLUMN id SET DEFAULT nextval('public.jobs_companies_id_seq'::regclass);


--
-- Name: jobs_descriptions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_descriptions ALTER COLUMN id SET DEFAULT nextval('public.jobs_descriptions_id_seq'::regclass);


--
-- Name: jobs_keyphrases id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keyphrases ALTER COLUMN id SET DEFAULT nextval('public.jobs_keyphrases_id_seq'::regclass);


--
-- Name: jobs_keywords id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keywords ALTER COLUMN id SET DEFAULT nextval('public.jobs_keywords_id_seq'::regclass);


--
-- Name: jobs_locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_locations ALTER COLUMN id SET DEFAULT nextval('public.jobs_locations_id_seq'::regclass);


--
-- Name: locations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations ALTER COLUMN id SET DEFAULT nextval('public.locations_id_seq'::regclass);


--
-- Name: companies companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.companies
    ADD CONSTRAINT companies_pkey PRIMARY KEY (id);


--
-- Name: job_listings job_listings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_listings
    ADD CONSTRAINT job_listings_pkey PRIMARY KEY (id);


--
-- Name: jobs_companies jobs_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_companies
    ADD CONSTRAINT jobs_companies_pkey PRIMARY KEY (id);


--
-- Name: jobs_keyphrases jobs_keyphrases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keyphrases
    ADD CONSTRAINT jobs_keyphrases_pkey PRIMARY KEY (id);


--
-- Name: jobs_keywords jobs_keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keywords
    ADD CONSTRAINT jobs_keywords_pkey PRIMARY KEY (id);


--
-- Name: jobs_locations jobs_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_locations
    ADD CONSTRAINT jobs_locations_pkey PRIMARY KEY (id);


--
-- Name: locations locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT locations_pkey PRIMARY KEY (id);


--
-- Name: jobs_companies jobs_companies_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_companies
    ADD CONSTRAINT jobs_companies_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.companies(id);


--
-- Name: jobs_companies jobs_companies_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_companies
    ADD CONSTRAINT jobs_companies_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job_listings(id);


--
-- Name: jobs_descriptions jobs_descriptions_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_descriptions
    ADD CONSTRAINT jobs_descriptions_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job_listings(id);


--
-- Name: jobs_keyphrases jobs_keyphrases_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keyphrases
    ADD CONSTRAINT jobs_keyphrases_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job_listings(id);


--
-- Name: jobs_keywords jobs_keywords_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_keywords
    ADD CONSTRAINT jobs_keywords_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job_listings(id);


--
-- Name: jobs_locations jobs_locations_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_locations
    ADD CONSTRAINT jobs_locations_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job_listings(id);


--
-- Name: jobs_locations jobs_locations_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.jobs_locations
    ADD CONSTRAINT jobs_locations_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- PostgreSQL database dump complete
--

