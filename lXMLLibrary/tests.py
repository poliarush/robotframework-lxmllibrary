import unittest
from keywords import XML
import lxml
import tempfile
import os

class TestlXMLLibrary(unittest.TestCase):

    """Test cases to test lXMLLibrary"""

    xml = """
		<example>
			<first id="1">text</first>
			<second id="2">
				<child/>
			</second>
			<third>
				<child>more text</child>
				<second id="child"/>
				<child><grandchild/></child>
			</third>
			<html>
				<p>
					Text with <b>bold</b> and <i>italics</i>
				</p>
			</html>
		</example>
		"""

    def setUp(self):
        self.lib = XML()
        self.xml_obj = self.lib.parse_xml(self.xml)

    def test_load_xml_from_string(self):
        self.assertIsInstance(self.xml_obj, lxml.etree._Element)
        self.assertEqual(self.lib.get_element_text(self.xml_obj, 
            "//child[following::*[contains(@id, 'child')] and ancestor::third]"), 
            "more text")

    def test_load_xml_from_file(self):
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(self.xml)
        temp.close()
        self.xml_obj = self.lib.parse_xml(temp.name)
        self.assertIsInstance(self.xml_obj, lxml.etree._Element)
        self.assertEqual(self.lib.get_element_text(self.xml_obj, 
            "//child[following::*[contains(@id, 'child')] and ancestor::third]"), 
            "more text")
        os.unlink(temp.name)

    def test_set_element_text(self):
        xml = self.lib.set_element_text(self.xml_obj, 
                "new_tag_name", 
                xpath="//*[@id='1' and contains(text(),'text')]")
        self.assertEqual(self.lib.get_element(xml, 
            "//*[@id='1' and contains(text(),'new_tag_name')]").text, 
            "new_tag_name")

    def test_set_element_tag(self):
        xml = self.lib.set_element_tag(self.xml_obj, 
                "new_tag_name", 
                "//*[@id='1' and contains(text(),'text')]")
        self.assertEqual(self.lib.get_element(xml, "//new_tag_name").text, 'text')

    def test_set_elements_text(self):
        xml = self.lib.set_elements_text(self.xml_obj, 
                "new_text", 
                xpath="//*")
        for element in self.lib.get_elements(xml, "//*"):
            self.assertEquals(element.text, "new_text")

    def test_set_elements_tag(self):
        xml = self.lib.set_elements_tag(self.xml_obj, 
                "new_tag", 
                xpath="//*[contains(local-name(.), 'child')]")
        for element in self.lib.get_elements(xml, "//*[contains(local-name(.), 'child')]"):
            self.assertEquals(element.tag, "new_tag1")

    def test_set_elements_attribute(self):
        xml = self.lib.set_elements_attribute(self.xml_obj, 
                "new_attribute", "new_value", 
                xpath="//*[contains(local-name(.), 'child')]")
        for element in self.lib.get_elements(xml, "//*[contains(local-name(.), 'child')]"):
            self.assertIn("new_attribute", element.attrib)

    def test_set_elements_text_from_file(self):
        pass

    def test_set_elements_text_from_dictionary(self):
        pass

    def test_get_element(self):
        element = self.lib.get_element(self.xml_obj, 
            "//*[@id='1']/following::i[preceding-sibling::b]")
        self.assertIsInstance(element, lxml.etree._Element)
        self.assertEqual(element.text, "italics")

    def test_get_element_with_xpath_on_multiple_nodes(self):
        with self.assertRaises(AssertionError):
            element = self.lib.get_element(self.xml_obj, 
            "//*[contains(local-name(.), 'child')]")

    def test_get_element_text(self):
        self.assertEqual(self.lib.get_element_text(self.xml_obj, 
            "//child[following::*[contains(@id, 'child')] and ancestor::third]"), 
            "more text")

    def test_get_elements(self):
        elements = self.lib.get_elements(self.xml_obj, 
            "//*[contains(local-name(.), 'child')]")
        self.assertSequenceEqual([i.tag for i in elements], 
            ['child', 'child', 'child', 'grandchild'])

if __name__ == '__main__':
    unittest.main()
