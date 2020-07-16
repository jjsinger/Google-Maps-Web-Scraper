# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv

HEADER = ['id_review', 'company_name', 'caption', 'timestamp', 'retrieval_date', 'rating', 'username', 'tot_user_reviews', 'n_review_user', 'n_photo_user', 'url_user'] #added company_name 6/22/2020
HEADER_W_SOURCE = ['id_review', 'company_name','caption', 'timestamp', 'retrieval_date', 'rating', 'username', 'tot_user_reviews', 'n_review_user', 'n_photo_user', 'url_user' 'url_source']


def csv_writer(source_field, path='data/', outfile='gm_reviews.csv'):
    targetfile = open(path + outfile, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)

    if source_field:
        h = HEADER_W_SOURCE
    else:
        h = HEADER
    writer.writerow(h)

    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--place', dest='place', action='store_true', help='Scrape place metadata')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Run scraper using browser graphical interface')
    parser.add_argument('--source', dest='source', action='store_true', help='Add source url to CSV file (for multiple urls in a single file)')
    parser.set_defaults(place=False, debug=False, source=False)

    args = parser.parse_args()

    # store reviews in CSV file
    writer = csv_writer(args.source)
    # print(args.source)
    
    with GoogleMapsScraper(debug=args.debug) as scraper:
        #maps_url = scraper.open_browser()
        
        with open(args.i, 'r+') as urls_file:
            print('... File is opened and ready to write...')
            #urls_file.write(maps_url)
            for url in urls_file:
                print(url)
                print(url.split('/'))
                if args.place:
                    # print('test')
                    print('URL: ', scraper.get_account(url))
                else:
                    error = scraper.sort_by_date(url)
                    print('ERROR CHECK: ', error)
                    if error == 0:

                        n = 0
                        while n < args.N:
                            reviews = scraper.get_reviews(n)

                            for r in reviews:
                                row_data = list(r.values())
                                if args.source:
                                    row_data.append(url)

                                writer.writerow(row_data)

                            n += len(reviews)
