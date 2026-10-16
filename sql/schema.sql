--
-- PostgreSQL database dump
--

\restrict vI0hlvNQScVRs9JO5jNYDazoLMlScu9jr0Sc3PssD1OhTTozN6njjyXlu4SzOUC

-- Dumped from database version 18.4 (Debian 18.4-1+b1)
-- Dumped by pg_dump version 18.4 (Debian 18.4-1+b1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ingestion_runs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ingestion_runs (
    id bigint NOT NULL,
    batch_id uuid NOT NULL,
    source_file text NOT NULL,
    started_at timestamp without time zone NOT NULL,
    completed_at timestamp without time zone,
    records_received integer DEFAULT 0,
    records_loaded integer DEFAULT 0,
    records_quarantined integer DEFAULT 0,
    status character varying(20) NOT NULL
);


--
-- Name: ingestion_runs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ingestion_runs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ingestion_runs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ingestion_runs_id_seq OWNED BY public.ingestion_runs.id;


--
-- Name: security_alerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.security_alerts (
    id bigint NOT NULL,
    source_ip inet NOT NULL,
    event_count integer CONSTRAINT security_alerts_failed_attempts_not_null NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    reason text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    username text
);


--
-- Name: security_alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.security_alerts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: security_alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.security_alerts_id_seq OWNED BY public.security_alerts.id;


--
-- Name: security_event_quarantine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.security_event_quarantine (
    id bigint NOT NULL,
    "timestamp" text,
    username text,
    source_ip text,
    event_type text,
    status text,
    issue_type character varying(100) NOT NULL,
    issue_description text NOT NULL,
    quarantined_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    source_file text,
    source_row_number integer
);


--
-- Name: security_event_quarantine_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.security_event_quarantine_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: security_event_quarantine_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.security_event_quarantine_id_seq OWNED BY public.security_event_quarantine.id;


--
-- Name: security_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.security_events (
    id bigint NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    username character varying(100) NOT NULL,
    source_ip inet NOT NULL,
    event_type character varying(50) NOT NULL,
    status character varying(20) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    ingestion_batch_id uuid,
    source_file text,
    source_row_number integer,
    ingested_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: security_events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.security_events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: security_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.security_events_id_seq OWNED BY public.security_events.id;


--
-- Name: ingestion_runs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingestion_runs ALTER COLUMN id SET DEFAULT nextval('public.ingestion_runs_id_seq'::regclass);


--
-- Name: security_alerts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_alerts ALTER COLUMN id SET DEFAULT nextval('public.security_alerts_id_seq'::regclass);


--
-- Name: security_event_quarantine id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_event_quarantine ALTER COLUMN id SET DEFAULT nextval('public.security_event_quarantine_id_seq'::regclass);


--
-- Name: security_events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events ALTER COLUMN id SET DEFAULT nextval('public.security_events_id_seq'::regclass);


--
-- Name: ingestion_runs ingestion_runs_batch_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingestion_runs
    ADD CONSTRAINT ingestion_runs_batch_id_key UNIQUE (batch_id);


--
-- Name: ingestion_runs ingestion_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingestion_runs
    ADD CONSTRAINT ingestion_runs_pkey PRIMARY KEY (id);


--
-- Name: security_alerts security_alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_alerts
    ADD CONSTRAINT security_alerts_pkey PRIMARY KEY (id);


--
-- Name: security_event_quarantine security_event_quarantine_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_event_quarantine
    ADD CONSTRAINT security_event_quarantine_pkey PRIMARY KEY (id);


--
-- Name: security_events security_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT security_events_pkey PRIMARY KEY (id);


--
-- Name: security_alerts unique_security_alert; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_alerts
    ADD CONSTRAINT unique_security_alert UNIQUE (source_ip, start_time, end_time, reason);


--
-- Name: security_events unique_source_record; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.security_events
    ADD CONSTRAINT unique_source_record UNIQUE (source_file, source_row_number);


--
-- Name: idx_security_alerts_source_ip; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_alerts_source_ip ON public.security_alerts USING btree (source_ip);


--
-- Name: idx_security_alerts_start_time; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_alerts_start_time ON public.security_alerts USING btree (start_time);


--
-- Name: idx_security_events_batch_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_events_batch_id ON public.security_events USING btree (ingestion_batch_id);


--
-- Name: idx_security_events_event_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_events_event_type ON public.security_events USING btree (event_type);


--
-- Name: idx_security_events_source_file; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_events_source_file ON public.security_events USING btree (source_file);


--
-- Name: idx_security_events_source_ip; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_events_source_ip ON public.security_events USING btree (source_ip);


--
-- Name: idx_security_events_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_security_events_timestamp ON public.security_events USING btree ("timestamp");


--
-- Name: unique_quarantine_source_record; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_quarantine_source_record ON public.security_event_quarantine USING btree (source_file, source_row_number);


--
-- PostgreSQL database dump complete
--

\unrestrict vI0hlvNQScVRs9JO5jNYDazoLMlScu9jr0Sc3PssD1OhTTozN6njjyXlu4SzOUC

