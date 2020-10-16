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
-- SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: image_metadata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.image_metadata (
    file_name character varying(255) NOT NULL,
    file_path character varying(255),
    patient_orientation character varying(255),
    view_position character varying(255),
    modality character(2),
    bits_stored smallint,
    photometric_interpretation character varying(255),
    window_center integer,
    window_width integer
);


ALTER TABLE public.image_metadata OWNER TO postgres;

--
-- Data for Name: image_metadata; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.image_metadata VALUES ('5_IM-2117-1003002.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/5/5_IM-2117-1003002.dcm', '', '', 'CR', 10, 'MONOCHROME1', NULL, NULL);
INSERT INTO public.image_metadata VALUES ('5_IM-2117-1004003.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/5/5_IM-2117-1004003.dcm', '', '', 'CR', 10, 'MONOCHROME1', NULL, NULL);
INSERT INTO public.image_metadata VALUES ('2_IM-0652-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/2/2_IM-0652-1001.dcm', '', '', 'CR', 12, 'MONOCHROME2', 3134, 1646);
INSERT INTO public.image_metadata VALUES ('2_IM-0652-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/2/2_IM-0652-2001.dcm', '', '', 'CR', 12, 'MONOCHROME2', 2626, 1440);
INSERT INTO public.image_metadata VALUES ('4_IM-2050-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/4/4_IM-2050-2001.dcm', 'L\F', 'PA', 'CR', 12, 'MONOCHROME1', NULL, NULL);
INSERT INTO public.image_metadata VALUES ('4_IM-2050-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/4/4_IM-2050-1001.dcm', 'L\F', 'PA', 'CR', 12, 'MONOCHROME1', NULL, NULL);
INSERT INTO public.image_metadata VALUES ('3_IM-1384-1001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/3/3_IM-1384-1001.dcm', '', '', 'CR', 12, 'MONOCHROME2', 3320, 1668);
INSERT INTO public.image_metadata VALUES ('3_IM-1384-2001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/3/3_IM-1384-2001.dcm', '', '', 'CR', 12, 'MONOCHROME2', 4096, 2048);
INSERT INTO public.image_metadata VALUES ('1_IM-0001-3001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/1/1_IM-0001-3001.dcm', 'L\F', 'PA', 'CR', 15, 'MONOCHROME1', NULL, NULL);
INSERT INTO public.image_metadata VALUES ('1_IM-0001-4001.dcm', 'NLMCXR_subset_dataset/NLMCXR_subset_dataset/1/1_IM-0001-4001.dcm', 'L\F', 'PA', 'CR', 15, 'MONOCHROME1', NULL, NULL);


--
-- Name: image_metadata image_metadata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.image_metadata
    ADD CONSTRAINT image_metadata_pkey PRIMARY KEY (file_name);


--
-- PostgreSQL database dump complete
--

