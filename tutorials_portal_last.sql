--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7
-- Dumped by pg_dump version 14.7

-- Started on 2025-04-07 16:23:53

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

SET default_table_access_method = heap;

--
-- TOC entry 222 (class 1259 OID 18331)
-- Name: answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.answers (
    id integer NOT NULL,
    question_id integer NOT NULL,
    answer_text text NOT NULL,
    is_correct boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.answers OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 18330)
-- Name: answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answers_id_seq OWNER TO postgres;

--
-- TOC entry 3513 (class 0 OID 0)
-- Dependencies: 221
-- Name: answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.answers_id_seq OWNED BY public.answers.id;


--
-- TOC entry 228 (class 1259 OID 18388)
-- Name: assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assignments (
    id integer NOT NULL,
    course_id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    due_date timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.assignments OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 18387)
-- Name: assignments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assignments_id_seq OWNER TO postgres;

--
-- TOC entry 3516 (class 0 OID 0)
-- Dependencies: 227
-- Name: assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assignments_id_seq OWNED BY public.assignments.id;


--
-- TOC entry 226 (class 1259 OID 18366)
-- Name: attempt_answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.attempt_answers (
    id integer NOT NULL,
    attempt_id integer NOT NULL,
    question_id integer NOT NULL,
    selected_answer_id integer NOT NULL
);


ALTER TABLE public.attempt_answers OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 18365)
-- Name: attempt_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.attempt_answers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attempt_answers_id_seq OWNER TO postgres;

--
-- TOC entry 3519 (class 0 OID 0)
-- Dependencies: 225
-- Name: attempt_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.attempt_answers_id_seq OWNED BY public.attempt_answers.id;


--
-- TOC entry 212 (class 1259 OID 18250)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 18249)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO postgres;

--
-- TOC entry 3522 (class 0 OID 0)
-- Dependencies: 211
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 238 (class 1259 OID 18486)
-- Name: course_progress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course_progress (
    id integer NOT NULL,
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    lesson_id integer NOT NULL,
    completed_at timestamp without time zone
);


ALTER TABLE public.course_progress OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 18485)
-- Name: course_progress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_progress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.course_progress_id_seq OWNER TO postgres;

--
-- TOC entry 3525 (class 0 OID 0)
-- Dependencies: 237
-- Name: course_progress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_progress_id_seq OWNED BY public.course_progress.id;


--
-- TOC entry 214 (class 1259 OID 18259)
-- Name: courses; Type: TABLE; Schema: public; Owner: tutorial_portal
--

CREATE TABLE public.courses (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text NOT NULL,
    teacher_id integer NOT NULL,
    price numeric(10,2) NOT NULL,
    language character varying(50) NOT NULL,
    level character varying(50) NOT NULL,
    category_id integer,
    thumbnail text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT courses_level_check CHECK (((level)::text = ANY ((ARRAY['Beginner'::character varying, 'Intermediate'::character varying, 'Advanced'::character varying])::text[]))),
    CONSTRAINT courses_price_check CHECK ((price >= (0)::numeric))
);


ALTER TABLE public.courses OWNER TO tutorial_portal;

--
-- TOC entry 213 (class 1259 OID 18258)
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: tutorial_portal
--

CREATE SEQUENCE public.courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.courses_id_seq OWNER TO tutorial_portal;

--
-- TOC entry 3527 (class 0 OID 0)
-- Dependencies: 213
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tutorial_portal
--

ALTER SEQUENCE public.courses_id_seq OWNED BY public.courses.id;


--
-- TOC entry 232 (class 1259 OID 18425)
-- Name: enrollments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrollments (
    id integer NOT NULL,
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    enrolled_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.enrollments OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 18424)
-- Name: enrollments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrollments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.enrollments_id_seq OWNER TO postgres;

--
-- TOC entry 3529 (class 0 OID 0)
-- Dependencies: 231
-- Name: enrollments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrollments_id_seq OWNED BY public.enrollments.id;


--
-- TOC entry 216 (class 1259 OID 18282)
-- Name: lessons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lessons (
    id integer NOT NULL,
    course_id integer NOT NULL,
    title character varying(255) NOT NULL,
    content_type character varying(50) NOT NULL,
    content_url text,
    text_content text,
    duration interval,
    "order" integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT lessons_content_type_check CHECK (((content_type)::text = ANY ((ARRAY['video'::character varying, 'pdf'::character varying, 'text'::character varying])::text[])))
);


ALTER TABLE public.lessons OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 18281)
-- Name: lessons_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.lessons_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.lessons_id_seq OWNER TO postgres;

--
-- TOC entry 3532 (class 0 OID 0)
-- Dependencies: 215
-- Name: lessons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.lessons_id_seq OWNED BY public.lessons.id;


--
-- TOC entry 236 (class 1259 OID 18466)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    student_id integer NOT NULL,
    course_id integer NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_status character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_amount_check CHECK ((amount >= (0)::numeric)),
    CONSTRAINT orders_payment_status_check CHECK (((payment_status)::text = ANY ((ARRAY['pending'::character varying, 'completed'::character varying, 'failed'::character varying])::text[])))
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 18465)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- TOC entry 3535 (class 0 OID 0)
-- Dependencies: 235
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- TOC entry 220 (class 1259 OID 18315)
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id integer NOT NULL,
    quiz_id integer NOT NULL,
    question_text text NOT NULL,
    question_type character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT questions_question_type_check CHECK (((question_type)::text = ANY ((ARRAY['multiple_choice'::character varying, 'true_false'::character varying])::text[])))
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 18314)
-- Name: questions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.questions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.questions_id_seq OWNER TO postgres;

--
-- TOC entry 3538 (class 0 OID 0)
-- Dependencies: 219
-- Name: questions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.questions_id_seq OWNED BY public.questions.id;


--
-- TOC entry 224 (class 1259 OID 18347)
-- Name: quiz_attempts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quiz_attempts (
    id integer NOT NULL,
    quiz_id integer NOT NULL,
    student_id integer NOT NULL,
    score numeric(5,2),
    attempted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT quiz_attempts_score_check CHECK ((score >= (0)::numeric))
);


ALTER TABLE public.quiz_attempts OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 18346)
-- Name: quiz_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quiz_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quiz_attempts_id_seq OWNER TO postgres;

--
-- TOC entry 3541 (class 0 OID 0)
-- Dependencies: 223
-- Name: quiz_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quiz_attempts_id_seq OWNED BY public.quiz_attempts.id;


--
-- TOC entry 218 (class 1259 OID 18299)
-- Name: quizzes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quizzes (
    id integer NOT NULL,
    course_id integer NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.quizzes OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 18298)
-- Name: quizzes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quizzes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quizzes_id_seq OWNER TO postgres;

--
-- TOC entry 3544 (class 0 OID 0)
-- Dependencies: 217
-- Name: quizzes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quizzes_id_seq OWNED BY public.quizzes.id;


--
-- TOC entry 234 (class 1259 OID 18445)
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    course_id integer NOT NULL,
    student_id integer NOT NULL,
    rating integer NOT NULL,
    comment text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reviews_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 18444)
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_id_seq OWNER TO postgres;

--
-- TOC entry 3547 (class 0 OID 0)
-- Dependencies: 233
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- TOC entry 230 (class 1259 OID 18404)
-- Name: submissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submissions (
    id integer NOT NULL,
    assignment_id integer NOT NULL,
    student_id integer NOT NULL,
    submission_file text NOT NULL,
    submission_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    grade numeric(5,2),
    feedback text,
    graded_at timestamp without time zone,
    CONSTRAINT submissions_grade_check CHECK (((grade >= (0)::numeric) AND (grade <= (100)::numeric)))
);


ALTER TABLE public.submissions OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 18403)
-- Name: submissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submissions_id_seq OWNER TO postgres;

--
-- TOC entry 3550 (class 0 OID 0)
-- Dependencies: 229
-- Name: submissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submissions_id_seq OWNED BY public.submissions.id;


--
-- TOC entry 210 (class 1259 OID 18236)
-- Name: users; Type: TABLE; Schema: public; Owner: tutorial_portal
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(50) NOT NULL,
    profile_picture text,
    bio text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['teacher'::character varying, 'student'::character varying, 'admin'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO tutorial_portal;

--
-- TOC entry 209 (class 1259 OID 18235)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: tutorial_portal
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO tutorial_portal;

--
-- TOC entry 3552 (class 0 OID 0)
-- Dependencies: 209
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tutorial_portal
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 3258 (class 2604 OID 18334)
-- Name: answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers ALTER COLUMN id SET DEFAULT nextval('public.answers_id_seq'::regclass);


--
-- TOC entry 3265 (class 2604 OID 18391)
-- Name: assignments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignments ALTER COLUMN id SET DEFAULT nextval('public.assignments_id_seq'::regclass);


--
-- TOC entry 3264 (class 2604 OID 18369)
-- Name: attempt_answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attempt_answers ALTER COLUMN id SET DEFAULT nextval('public.attempt_answers_id_seq'::regclass);


--
-- TOC entry 3240 (class 2604 OID 18253)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 3280 (class 2604 OID 18489)
-- Name: course_progress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_progress ALTER COLUMN id SET DEFAULT nextval('public.course_progress_id_seq'::regclass);


--
-- TOC entry 3243 (class 2604 OID 18262)
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.courses ALTER COLUMN id SET DEFAULT nextval('public.courses_id_seq'::regclass);


--
-- TOC entry 3271 (class 2604 OID 18428)
-- Name: enrollments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments ALTER COLUMN id SET DEFAULT nextval('public.enrollments_id_seq'::regclass);


--
-- TOC entry 3248 (class 2604 OID 18285)
-- Name: lessons id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons ALTER COLUMN id SET DEFAULT nextval('public.lessons_id_seq'::regclass);


--
-- TOC entry 3276 (class 2604 OID 18469)
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- TOC entry 3255 (class 2604 OID 18318)
-- Name: questions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions ALTER COLUMN id SET DEFAULT nextval('public.questions_id_seq'::regclass);


--
-- TOC entry 3261 (class 2604 OID 18350)
-- Name: quiz_attempts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts ALTER COLUMN id SET DEFAULT nextval('public.quiz_attempts_id_seq'::regclass);


--
-- TOC entry 3252 (class 2604 OID 18302)
-- Name: quizzes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes ALTER COLUMN id SET DEFAULT nextval('public.quizzes_id_seq'::regclass);


--
-- TOC entry 3273 (class 2604 OID 18448)
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- TOC entry 3268 (class 2604 OID 18407)
-- Name: submissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions ALTER COLUMN id SET DEFAULT nextval('public.submissions_id_seq'::regclass);


--
-- TOC entry 3236 (class 2604 OID 18239)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 3490 (class 0 OID 18331)
-- Dependencies: 222
-- Data for Name: answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.answers (id, question_id, answer_text, is_correct, created_at) FROM stdin;
\.


--
-- TOC entry 3496 (class 0 OID 18388)
-- Dependencies: 228
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.assignments (id, course_id, title, description, due_date, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 3494 (class 0 OID 18366)
-- Dependencies: 226
-- Data for Name: attempt_answers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.attempt_answers (id, attempt_id, question_id, selected_answer_id) FROM stdin;
\.


--
-- TOC entry 3480 (class 0 OID 18250)
-- Dependencies: 212
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, created_at, updated_at) FROM stdin;
1	IELTS	2025-01-12 11:26:38.055278	2025-01-12 11:26:38.055278
2	IT & Telecommunications	2025-01-12 11:26:47.450296	2025-01-12 11:27:02.826564
3	Programming	2025-01-13 09:54:23.774763	2025-01-13 09:54:23.774763
4	Networking	2025-01-13 09:54:32.136853	2025-01-13 09:57:07.950916
5	Machine Learning	2025-01-13 09:57:23.796067	2025-01-13 09:57:23.796067
6	Software Engineering	2025-01-15 16:33:07.595072	2025-01-15 16:33:07.595072
\.


--
-- TOC entry 3506 (class 0 OID 18486)
-- Dependencies: 238
-- Data for Name: course_progress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.course_progress (id, student_id, course_id, lesson_id, completed_at) FROM stdin;
\.


--
-- TOC entry 3482 (class 0 OID 18259)
-- Dependencies: 214
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: tutorial_portal
--

COPY public.courses (id, title, description, teacher_id, price, language, level, category_id, thumbnail, created_at, updated_at) FROM stdin;
4	Introduction to Machine Learning	First Machine Learning Course	1	100.00	English, Bangla	Intermediate	5	4_brain.png	2025-01-15 05:57:36.017193	2025-01-15 06:02:40.260333
5	DOT NET Programming	DOT NET Programming	1	120.00	English, Bangla	Beginner	3	5_social.png	2025-01-15 06:18:43.967628	2025-01-15 06:18:43.97515
6	C#  Programming	C#  Programming	8	100.00	English, French	Beginner	3	6_social.png	2025-01-15 10:35:16.608429	2025-01-15 10:35:16.676484
\.


--
-- TOC entry 3500 (class 0 OID 18425)
-- Dependencies: 232
-- Data for Name: enrollments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enrollments (id, student_id, course_id, enrolled_at) FROM stdin;
\.


--
-- TOC entry 3484 (class 0 OID 18282)
-- Dependencies: 216
-- Data for Name: lessons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lessons (id, course_id, title, content_type, content_url, video_url, duration, "order", created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 3504 (class 0 OID 18466)
-- Dependencies: 236
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, student_id, course_id, amount, payment_status, created_at) FROM stdin;
\.


--
-- TOC entry 3488 (class 0 OID 18315)
-- Dependencies: 220
-- Data for Name: questions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.questions (id, quiz_id, question_text, question_type, created_at) FROM stdin;
\.


--
-- TOC entry 3492 (class 0 OID 18347)
-- Dependencies: 224
-- Data for Name: quiz_attempts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quiz_attempts (id, quiz_id, student_id, score, attempted_at) FROM stdin;
\.


--
-- TOC entry 3486 (class 0 OID 18299)
-- Dependencies: 218
-- Data for Name: quizzes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quizzes (id, course_id, title, description, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 3502 (class 0 OID 18445)
-- Dependencies: 234
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (id, course_id, student_id, rating, comment, created_at) FROM stdin;
\.


--
-- TOC entry 3498 (class 0 OID 18404)
-- Dependencies: 230
-- Data for Name: submissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submissions (id, assignment_id, student_id, submission_file, submission_date, grade, feedback, graded_at) FROM stdin;
\.


--
-- TOC entry 3478 (class 0 OID 18236)
-- Dependencies: 210
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: tutorial_portal
--

COPY public.users (id, name, email, password, role, profile_picture, bio, created_at, updated_at) FROM stdin;
2	Nadim	nadim1@gmail.com	pbkdf2:sha256:600000$aitLD5xYkPAq73nH$c6fa7143df7310ffa01c5fd8754a4b371e28f559c8b92e77c221e44890bfb0e6	student	fb8743ffc93f4df1a06b2eeab8209258_Aninda_Sen_cropped_2.jpg	Tell me about my taste	2025-01-07 10:49:14.733884	2025-01-07 10:49:14.733884
1	Golam Mostofa	mostofa1@gmail.com	pbkdf2:sha256:600000$OTyJwBbCtvlU2C3U$9e122f8ce007f60953d6398a9169f9737a2aa28464bf6ef6ae5eb1d28042dafe	teacher	ee61cca64f774847a9e901011e40a3cd_man.png	A Fulltime Instructor	2025-01-07 10:41:30.009242	2025-01-07 10:41:30.009242
7	admin	admin@gmail.com	pbkdf2:sha256:600000$GBbHpIXGBgOE7ykS$488741f6e6df02c5368e382f9482a539353a8df646e5bcb5e97ea1f735b0c181	admin	4893a87d978b49398bd960157599efb8_man.png	He is a Good Admin and Good Height Person	2025-01-07 11:41:58.512778	2025-01-07 11:41:58.512778
8	Arafat Hossain	arafat@gmail.com	pbkdf2:sha256:600000$u2eqlLgldD5Z5o3L$ec1fd11d181db5402126e028c7864841b6f05d6348fd4cbcbabb38101c9f2f4c	teacher	\N	\N	2025-01-15 16:34:09.142098	2025-01-15 16:34:09.142098
9	Shemul	shemul@gmail.com	pbkdf2:sha256:600000$Wrkr0oHGe7PJDhOz$8134e595e2105ebd70bab1c4529d1b55cdf9a482abbde0131c4746c96253504a	student	6b420c2c6f684a928f6c7db8b78917a2_Aninda_Sen_cropped_2.jpg	Excellent	2025-01-15 16:35:53.421134	2025-01-15 16:35:53.421134
\.


--
-- TOC entry 3553 (class 0 OID 0)
-- Dependencies: 221
-- Name: answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.answers_id_seq', 1, false);


--
-- TOC entry 3554 (class 0 OID 0)
-- Dependencies: 227
-- Name: assignments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.assignments_id_seq', 1, false);


--
-- TOC entry 3555 (class 0 OID 0)
-- Dependencies: 225
-- Name: attempt_answers_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.attempt_answers_id_seq', 1, false);


--
-- TOC entry 3556 (class 0 OID 0)
-- Dependencies: 211
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, true);


--
-- TOC entry 3557 (class 0 OID 0)
-- Dependencies: 237
-- Name: course_progress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.course_progress_id_seq', 1, false);


--
-- TOC entry 3558 (class 0 OID 0)
-- Dependencies: 213
-- Name: courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tutorial_portal
--

SELECT pg_catalog.setval('public.courses_id_seq', 6, true);


--
-- TOC entry 3559 (class 0 OID 0)
-- Dependencies: 231
-- Name: enrollments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.enrollments_id_seq', 1, false);


--
-- TOC entry 3560 (class 0 OID 0)
-- Dependencies: 215
-- Name: lessons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.lessons_id_seq', 1, false);


--
-- TOC entry 3561 (class 0 OID 0)
-- Dependencies: 235
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- TOC entry 3562 (class 0 OID 0)
-- Dependencies: 219
-- Name: questions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.questions_id_seq', 1, false);


--
-- TOC entry 3563 (class 0 OID 0)
-- Dependencies: 223
-- Name: quiz_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quiz_attempts_id_seq', 1, false);


--
-- TOC entry 3564 (class 0 OID 0)
-- Dependencies: 217
-- Name: quizzes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quizzes_id_seq', 1, false);


--
-- TOC entry 3565 (class 0 OID 0)
-- Dependencies: 233
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reviews_id_seq', 1, false);


--
-- TOC entry 3566 (class 0 OID 0)
-- Dependencies: 229
-- Name: submissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submissions_id_seq', 1, false);


--
-- TOC entry 3567 (class 0 OID 0)
-- Dependencies: 209
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tutorial_portal
--

SELECT pg_catalog.setval('public.users_id_seq', 9, true);


--
-- TOC entry 3296 (class 2606 OID 18340)
-- Name: answers answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_pkey PRIMARY KEY (id);


--
-- TOC entry 3302 (class 2606 OID 18397)
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 18371)
-- Name: attempt_answers attempt_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attempt_answers
    ADD CONSTRAINT attempt_answers_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2606 OID 18257)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 3314 (class 2606 OID 18491)
-- Name: course_progress course_progress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_progress
    ADD CONSTRAINT course_progress_pkey PRIMARY KEY (id);


--
-- TOC entry 3288 (class 2606 OID 18270)
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- TOC entry 3306 (class 2606 OID 18431)
-- Name: enrollments enrollments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_pkey PRIMARY KEY (id);


--
-- TOC entry 3308 (class 2606 OID 18433)
-- Name: enrollments enrollments_student_id_course_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_student_id_course_id_key UNIQUE (student_id, course_id);


--
-- TOC entry 3290 (class 2606 OID 18292)
-- Name: lessons lessons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_pkey PRIMARY KEY (id);


--
-- TOC entry 3312 (class 2606 OID 18474)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 3294 (class 2606 OID 18324)
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- TOC entry 3298 (class 2606 OID 18354)
-- Name: quiz_attempts quiz_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_pkey PRIMARY KEY (id);


--
-- TOC entry 3292 (class 2606 OID 18308)
-- Name: quizzes quizzes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_pkey PRIMARY KEY (id);


--
-- TOC entry 3310 (class 2606 OID 18454)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- TOC entry 3304 (class 2606 OID 18413)
-- Name: submissions submissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_pkey PRIMARY KEY (id);


--
-- TOC entry 3282 (class 2606 OID 18248)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 3284 (class 2606 OID 18246)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 3320 (class 2606 OID 18341)
-- Name: answers answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.answers
    ADD CONSTRAINT answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;


--
-- TOC entry 3326 (class 2606 OID 18398)
-- Name: assignments assignments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3323 (class 2606 OID 18372)
-- Name: attempt_answers attempt_answers_attempt_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attempt_answers
    ADD CONSTRAINT attempt_answers_attempt_id_fkey FOREIGN KEY (attempt_id) REFERENCES public.quiz_attempts(id) ON DELETE CASCADE;


--
-- TOC entry 3324 (class 2606 OID 18377)
-- Name: attempt_answers attempt_answers_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attempt_answers
    ADD CONSTRAINT attempt_answers_question_id_fkey FOREIGN KEY (question_id) REFERENCES public.questions(id) ON DELETE CASCADE;


--
-- TOC entry 3325 (class 2606 OID 18382)
-- Name: attempt_answers attempt_answers_selected_answer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.attempt_answers
    ADD CONSTRAINT attempt_answers_selected_answer_id_fkey FOREIGN KEY (selected_answer_id) REFERENCES public.answers(id) ON DELETE CASCADE;


--
-- TOC entry 3335 (class 2606 OID 18497)
-- Name: course_progress course_progress_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_progress
    ADD CONSTRAINT course_progress_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3336 (class 2606 OID 18502)
-- Name: course_progress course_progress_lesson_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_progress
    ADD CONSTRAINT course_progress_lesson_id_fkey FOREIGN KEY (lesson_id) REFERENCES public.lessons(id) ON DELETE CASCADE;


--
-- TOC entry 3337 (class 2606 OID 18492)
-- Name: course_progress course_progress_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_progress
    ADD CONSTRAINT course_progress_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3315 (class 2606 OID 18276)
-- Name: courses courses_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- TOC entry 3316 (class 2606 OID 18271)
-- Name: courses courses_teacher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tutorial_portal
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3329 (class 2606 OID 18439)
-- Name: enrollments enrollments_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3330 (class 2606 OID 18434)
-- Name: enrollments enrollments_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrollments
    ADD CONSTRAINT enrollments_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3317 (class 2606 OID 18293)
-- Name: lessons lessons_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lessons
    ADD CONSTRAINT lessons_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3333 (class 2606 OID 18480)
-- Name: orders orders_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3334 (class 2606 OID 18475)
-- Name: orders orders_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3319 (class 2606 OID 18325)
-- Name: questions questions_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(id) ON DELETE CASCADE;


--
-- TOC entry 3321 (class 2606 OID 18355)
-- Name: quiz_attempts quiz_attempts_quiz_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_quiz_id_fkey FOREIGN KEY (quiz_id) REFERENCES public.quizzes(id) ON DELETE CASCADE;


--
-- TOC entry 3322 (class 2606 OID 18360)
-- Name: quiz_attempts quiz_attempts_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempts
    ADD CONSTRAINT quiz_attempts_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3318 (class 2606 OID 18309)
-- Name: quizzes quizzes_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quizzes
    ADD CONSTRAINT quizzes_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3331 (class 2606 OID 18455)
-- Name: reviews reviews_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(id) ON DELETE CASCADE;


--
-- TOC entry 3332 (class 2606 OID 18460)
-- Name: reviews reviews_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3327 (class 2606 OID 18414)
-- Name: submissions submissions_assignment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_assignment_id_fkey FOREIGN KEY (assignment_id) REFERENCES public.assignments(id) ON DELETE CASCADE;


--
-- TOC entry 3328 (class 2606 OID 18419)
-- Name: submissions submissions_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submissions
    ADD CONSTRAINT submissions_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 3512 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE answers; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.answers TO tutorial_portal;


--
-- TOC entry 3514 (class 0 OID 0)
-- Dependencies: 221
-- Name: SEQUENCE answers_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.answers_id_seq TO tutorial_portal;


--
-- TOC entry 3515 (class 0 OID 0)
-- Dependencies: 228
-- Name: TABLE assignments; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.assignments TO tutorial_portal;


--
-- TOC entry 3517 (class 0 OID 0)
-- Dependencies: 227
-- Name: SEQUENCE assignments_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.assignments_id_seq TO tutorial_portal;


--
-- TOC entry 3518 (class 0 OID 0)
-- Dependencies: 226
-- Name: TABLE attempt_answers; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.attempt_answers TO tutorial_portal;


--
-- TOC entry 3520 (class 0 OID 0)
-- Dependencies: 225
-- Name: SEQUENCE attempt_answers_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.attempt_answers_id_seq TO tutorial_portal;


--
-- TOC entry 3521 (class 0 OID 0)
-- Dependencies: 212
-- Name: TABLE categories; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.categories TO tutorial_portal;


--
-- TOC entry 3523 (class 0 OID 0)
-- Dependencies: 211
-- Name: SEQUENCE categories_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.categories_id_seq TO tutorial_portal;


--
-- TOC entry 3524 (class 0 OID 0)
-- Dependencies: 238
-- Name: TABLE course_progress; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.course_progress TO tutorial_portal;


--
-- TOC entry 3526 (class 0 OID 0)
-- Dependencies: 237
-- Name: SEQUENCE course_progress_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.course_progress_id_seq TO tutorial_portal;


--
-- TOC entry 3528 (class 0 OID 0)
-- Dependencies: 232
-- Name: TABLE enrollments; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.enrollments TO tutorial_portal;


--
-- TOC entry 3530 (class 0 OID 0)
-- Dependencies: 231
-- Name: SEQUENCE enrollments_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.enrollments_id_seq TO tutorial_portal;


--
-- TOC entry 3531 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE lessons; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.lessons TO tutorial_portal;


--
-- TOC entry 3533 (class 0 OID 0)
-- Dependencies: 215
-- Name: SEQUENCE lessons_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.lessons_id_seq TO tutorial_portal;


--
-- TOC entry 3534 (class 0 OID 0)
-- Dependencies: 236
-- Name: TABLE orders; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.orders TO tutorial_portal;


--
-- TOC entry 3536 (class 0 OID 0)
-- Dependencies: 235
-- Name: SEQUENCE orders_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.orders_id_seq TO tutorial_portal;


--
-- TOC entry 3537 (class 0 OID 0)
-- Dependencies: 220
-- Name: TABLE questions; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.questions TO tutorial_portal;


--
-- TOC entry 3539 (class 0 OID 0)
-- Dependencies: 219
-- Name: SEQUENCE questions_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.questions_id_seq TO tutorial_portal;


--
-- TOC entry 3540 (class 0 OID 0)
-- Dependencies: 224
-- Name: TABLE quiz_attempts; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.quiz_attempts TO tutorial_portal;


--
-- TOC entry 3542 (class 0 OID 0)
-- Dependencies: 223
-- Name: SEQUENCE quiz_attempts_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.quiz_attempts_id_seq TO tutorial_portal;


--
-- TOC entry 3543 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE quizzes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.quizzes TO tutorial_portal;


--
-- TOC entry 3545 (class 0 OID 0)
-- Dependencies: 217
-- Name: SEQUENCE quizzes_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.quizzes_id_seq TO tutorial_portal;


--
-- TOC entry 3546 (class 0 OID 0)
-- Dependencies: 234
-- Name: TABLE reviews; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.reviews TO tutorial_portal;


--
-- TOC entry 3548 (class 0 OID 0)
-- Dependencies: 233
-- Name: SEQUENCE reviews_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.reviews_id_seq TO tutorial_portal;


--
-- TOC entry 3549 (class 0 OID 0)
-- Dependencies: 230
-- Name: TABLE submissions; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.submissions TO tutorial_portal;


--
-- TOC entry 3551 (class 0 OID 0)
-- Dependencies: 229
-- Name: SEQUENCE submissions_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.submissions_id_seq TO tutorial_portal;


--
-- TOC entry 2096 (class 826 OID 18509)
-- Name: DEFAULT PRIVILEGES FOR FUNCTIONS; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON FUNCTIONS  TO tutorial_portal WITH GRANT OPTION;


--
-- TOC entry 2095 (class 826 OID 18508)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES  TO tutorial_portal WITH GRANT OPTION;


-- Completed on 2025-04-07 16:23:53

--
-- PostgreSQL database dump complete
--

