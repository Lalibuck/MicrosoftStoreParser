from parser import page_parser, category_parser


def test_category_parser(browser):
    test_links = ['https://apps.microsoft.com/store/detail/%D1%86%D0%B5%D0%BD%D1%82%D1%80-%D1%83%D0%BF%D1%80%D0%B0%D0'
                  '%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B3%D1%80%D0%B0%D1%84%D0%B8%D0%BA%D0%BE%D0%B9-intel%C2%AE'
                  '/9PLFNLNT3G5G', 'https://apps.microsoft.com/store/detail/pdf-x-%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1'
                                   '%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-pdf-%D0%BF%D1%80%D0%BE%D1%81'
                                   '%D0%BC%D0%BE%D1%82%D1%80-pdf/9P3CP9G025RM',
                  'https://apps.microsoft.com/store/detail/power-bi-desktop/9NTXR16HNW1T',
                  'https://apps.microsoft.com/store/detail/slack/9WZDNCRDK3WP',
                  'https://apps.microsoft.com/store/detail/citrix-workspace/9WZDNCRFJ2KJ',
                  'https://apps.microsoft.com/store/detail/%D0%BA%D0%BE%D1%80%D0%BF%D0%BE%D1%80%D0%B0%D1%82%D0%B8%D0'
                  '%B2%D0%BD%D1%8B%D0%B9-%D0%BF%D0%BE%D1%80%D1%82%D0%B0%D0%BB/9WZDNCRFJ3PZ',
                  'https://apps.microsoft.com/store/detail/neat-office-docs-pdf-app/9P2HTZQ722V3',
                  'https://apps.microsoft.com/store/detail/pdf-reader-elf-%D1%80%D0%B5%D0%B4%D0%B0%D0%BA%D1%82%D0%BE'
                  '%D1%80-pdf/9N2F0P0166HF', 'https://apps.microsoft.com/store/detail/zoom-rooms/9NH8747BW3BC',
                  'https://apps.microsoft.com/store/detail/pdf-merger-splitter/9P4TCNS9H432',
                  'https://apps.microsoft.com/store/detail/xodo-pdf-reader-editor/9WZDNCRDJXP4',
                  'https://apps.microsoft.com/store/detail/power-bi/9NBLGGGZLXN1',
                  'https://apps.microsoft.com/store/detail/trello/9NBLGGH4XXVW',
                  'https://apps.microsoft.com/store/detail/free-invoice-generator/9NBLGGH5NZB7',
                  'https://apps.microsoft.com/store/detail/diligent-boards/9WZDNCRDH8XD',
                  'https://apps.microsoft.com/store/detail/dropshipping-with-shopify-full-course/9PMBNF4T4MDB',
                  'https://apps.microsoft.com/store/detail/doc-opener-for-sell/9NCRLQSFHQWH',
                  'https://apps.microsoft.com/store/detail/any-doc-to-pdf/9N42NPLXMS72',
                  'https://apps.microsoft.com/store/detail/hp-enhanced-lighting/9N0Z0X2QTN0H',
                  'https://apps.microsoft.com/store/detail/pdf-suiter-open-find-print-pdf/9N0MRSN0D6LC']

    links = category_parser(browser, 20, 'Business')
    assert len(links) == len(test_links)
    for i in range(len(test_links)):
        assert test_links[i] == links[i]


def test_page_parser(browser):
    parsed_app = page_parser(browser, 'https://apps.microsoft.com/store/detail/taskade/9P1JH1D9BG26')
    assert parsed_app[0] == 'Taskade'
    assert parsed_app[1] == 'Taskcade Inc.'
    assert parsed_app[2] == '2020'
    assert parsed_app[3] == 'support@taskade.com'
