robotframework-lxmllibrary
==========================

RobotFramework lXMLLibrary to with full XPath 1.0 support thru lxml library

Problem
==========================
Existing RobotFramework XML library supports only simple XPath expression which is not enough for testing purposes.

Extra keywords added 
==========================
- get_elements_texts
- elements_text_should_be
- elements_text_should_match
- elements_text_should_match_regexp
- elements_should_match
- elements_should_be_equal
- elements_count_should_be_equal
- set_elements_attribute
- set_elements_tag
- set_elements_text


Aim
==========================
- clone XML library
- substitute ElementTree with lxml library as core engine for xml processing
- add keywords to set\check multiple nodes on text\tag\attribute 
- add unit tests for library
