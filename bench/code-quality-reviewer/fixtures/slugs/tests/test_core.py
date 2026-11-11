import unittest

from slugs.core import MAX_LEN, is_slug, slugify, unique_slug


class SlugifyTest(unittest.TestCase):
    def test_words_are_joined_by_single_hyphens(self):
        self.assertEqual(slugify("  Hello,   World! "), "hello-world")

    def test_non_ascii_letters_are_dropped(self):
        self.assertEqual(slugify("Café au lait"), "caf-au-lait")

    def test_a_long_title_is_cut_at_a_word(self):
        title = "word " * 30
        slug = slugify(title)
        self.assertLessEqual(len(slug), MAX_LEN)
        self.assertTrue(slug.endswith("word"))
        self.assertEqual(len(slug), 79)

    def test_a_cut_may_land_exactly_on_the_limit(self):
        title = "a" * 80 + " tail"
        self.assertEqual(slugify(title), "a" * 80)

    def test_one_very_long_word_is_cut_at_the_limit(self):
        self.assertEqual(slugify("x" * 200), "x" * MAX_LEN)

    def test_nothing_usable_gives_an_empty_slug(self):
        self.assertEqual(slugify("¡¿!?"), "")


class IsSlugTest(unittest.TestCase):
    def test_accepts_what_slugify_returns(self):
        for title in ("Hello, World!", "word " * 30, "x" * 200, "A-b_c"):
            self.assertTrue(is_slug(slugify(title)), title)

    def test_refuses_uppercase_edges_and_doubles(self):
        for text in ("Hello", "-a", "a-", "a--b", " a", "", "a" * 81, "a_b"):
            self.assertFalse(is_slug(text), text)


class UniqueSlugTest(unittest.TestCase):
    def test_the_plain_slug_when_it_is_free(self):
        self.assertEqual(unique_slug("Hello", set()), "hello")

    def test_a_number_is_added_when_it_is_taken(self):
        self.assertEqual(unique_slug("Hello", {"hello", "hello-2"}), "hello-3")

    def test_the_number_fits_inside_the_limit(self):
        base = "a" * 80
        slug = unique_slug(base, {base})
        self.assertEqual(slug, "a" * 78 + "-2")
        self.assertEqual(len(slug), MAX_LEN)

    def test_a_title_with_nothing_usable_is_refused(self):
        with self.assertRaises(ValueError):
            unique_slug("¡¿!?", set())
