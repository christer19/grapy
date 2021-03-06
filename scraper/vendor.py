import re
import logging
import logging.config
import plugins
from pprint import pformat
from django.db import IntegrityError
from wines import models
from . import scraper


logger = logging.getLogger(__name__)


class VendorScraper(scraper.Scraper):

    product_list = []

    def persist(self):
        logger.info('Persisting {} products'.format(len(self.product_list)))

        for product in self.product_list:
            vendor = models.Vendor.objects.get(pk=product['vendor_id'])

            logger.info('[{}] Add product:\n{}'.format(
                vendor.name,
                pformat(product)))

            try:
                wine, created = models.VendorWine.objects.update_or_create(
                    vendor=vendor,
                    url=product['url'],
                    defaults={
                        'vendor_code': product['code'],
                        'title': product['title'],
                        'volume': product['volume'],
                        'quantity': product['quantity'],
                        'price': product['price']
                    },
                )

                logger.info('[{}] {} vendorwine: {}'.format(
                    vendor.name,
                    'Created' if created else 'Updated',
                    wine.title))
            except KeyError as e:
                logger.error('KeyError creating {}: {}, see {}'.format(
                    product['title'],
                    e,
                    product['url']))
            except IntegrityError as e:
                logger.error('IntegrityError creating {}: {}, see {}'.format(
                    product['title'],
                    e,
                    product['url']))
            except Exception as e:
                logger.error('Error creating {}: {}, see {}'.format(
                    product['title'],
                    e,
                    product['url']))

    def is_valid(self, vendor, product):
        """ Validates a product """
        valid = True

        logger.info('[{}] Validating product {}'.format(
            vendor.name,
            product['title']))

        if vendor.stopwords != '':
            regex = re.compile(vendor.stopwords, re.I)
            match = re.search(regex, product['title'])

            if match:
                valid = False
                logger.warning('[{}] Skipped: product matches stopword {}'.format(
                    vendor.name,
                    vendor.stopwords))

        return valid

    def add(self, product):
        """ Add the product to the product list if valid """
        try:
            vendor = models.Vendor.objects.get(pk=product['vendor_id'])
        except models.Vendor.DoesNotExist as e:
            logger.warning('Unable to add product: {} {}'.format(
                e,
                product['vendor_id']))
            return
        except Exception as e:
            logger.warning('Unable to add product: {} {}'.format(
                e,
                product['vendor_id']))
            return

        if self.is_valid(vendor, product):
            self.product_list.append(product)
        else:
            logger.warning('[{}] Skipped invalid product: {}'.format(
                vendor.name,
                product['title']))

    def scrape(self):
        logger.debug(plugins.vendor_plugins)

        for vendor in models.Vendor.active.all():
            self.product_list = []

            logger.info('[{}] Loading config...'.format(
                vendor.name))

            try:
                module = plugins.vendor_plugins[vendor.plugin]
            except ModuleNotFoundError as e:
                logger.error(e)

            if module:
                config = {
                    'vendor_id': vendor.id,
                    'base_url': vendor.url,
                    'page': vendor.page,
                    'max_pages': vendor.max_pages,
                    'product': vendor.product,
                    'callback': self.add
                }
                logger.info('[{}] Starting plugin {}...'.format(
                    vendor.name,
                    module))
                module.init(config)

            # scraping done, persist list
            if not vendor.is_test:
                self.persist()
            else:
                path = 'products_{}.csv'.format(vendor.name)
                scraper.Scraper.to_csv(path, self.product_list)
                logger.info('[{}] Test mode: products saved to file {}'.format(
                    vendor.name,
                    path))
