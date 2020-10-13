--
-- PostgreSQL database dump
--

-- Dumped from database version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: image_labels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.image_labels (
    file_name character varying(255) NOT NULL,
    file_path character varying(255),
    image_view character(1)
);


ALTER TABLE public.image_labels OWNER TO postgres;

--
-- Data for Name: image_labels; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.image_labels VALUES ('1_IM-0001-3001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/1/1_IM-0001-3001.dcm', 'F');
INSERT INTO public.image_labels VALUES ('1_IM-0001-4001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/1/1_IM-0001-4001.dcm', 'L');
INSERT INTO public.image_labels VALUES ('2_IM-0652-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/2/2_IM-0652-1001.dcm', 'F');
INSERT INTO public.image_labels VALUES ('2_IM-0652-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/2/2_IM-0652-2001.dcm', 'L');
INSERT INTO public.image_labels VALUES ('3_IM-1384-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/3/3_IM-1384-1001.dcm', 'F');
INSERT INTO public.image_labels VALUES ('3_IM-1384-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/3/3_IM-1384-2001.dcm', 'L');
INSERT INTO public.image_labels VALUES ('4_IM-2050-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/4/4_IM-2050-1001.dcm', 'F');
INSERT INTO public.image_labels VALUES ('4_IM-2050-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/4/4_IM-2050-2001.dcm', 'L');
INSERT INTO public.image_labels VALUES ('5_IM-2117-1003002.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/5/5_IM-2117-1003002.dcm', 'F');
INSERT INTO public.image_labels VALUES ('5_IM-2117-1004003.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/5/5_IM-2117-1004003.dcm', 'L');


--
-- Name: image_labels image_labels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.image_labels
    ADD CONSTRAINT image_labels_pkey PRIMARY KEY (file_name);


--
-- PostgreSQL database dump complete
--

