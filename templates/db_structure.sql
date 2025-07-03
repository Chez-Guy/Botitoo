-- Use this file as a template to create a PostgreSQL database for the bot

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

--
-- TOC entry 3375 (class 1262 OID 16394)
-- Name: botitoo; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE botitoo WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_GB.UTF-8';


\connect botitoo

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
-- TOC entry 214 (class 1259 OID 16395)
-- Name: bad_weirdos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bad_weirdos (
    user_id bigint NOT NULL
);


--
-- TOC entry 219 (class 1259 OID 16418)
-- Name: custom_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.custom_roles (
    userid bigint,
    roleid bigint,
    invalid boolean,
    invalid_time bigint
);


--
-- TOC entry 215 (class 1259 OID 16398)
-- Name: media_share_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.media_share_users (
    id bigint NOT NULL,
    count integer NOT NULL,
    whitelisted boolean DEFAULT false NOT NULL
);


--
-- TOC entry 216 (class 1259 OID 16402)
-- Name: previous; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.previous (
    name character varying(255) DEFAULT NULL::character varying,
    storage character varying(255) DEFAULT NULL::character varying
);


--
-- TOC entry 217 (class 1259 OID 16409)
-- Name: submissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.submissions (
    id text NOT NULL,
    count smallint NOT NULL,
    whitelisted boolean DEFAULT false NOT NULL
);


--
-- TOC entry 218 (class 1259 OID 16415)
-- Name: weirdos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.weirdos (
    user_id bigint NOT NULL
);