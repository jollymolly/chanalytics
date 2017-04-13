from django.shortcuts import render
from django.urls import reverse

import os, functools

from .apps import ChanalyticsConfig
from .models import *

class GenericAnalyticsView:

    key_to_field_model_map = {
        'country_code': GeoAnalytics,
        'age_group': DemographicsAnalytics,
        'gender': DemographicsAnalytics,
        'device_type': DeviceAnalytics,
        'os': OSAnalytics
    }

    template_path = os.path.join(ChanalyticsConfig.name, 'default.html')

    def _getAvailableFormOptions(self):

        select_values = {}

        for k in self.key_to_field_model_map:
            mgr = self.key_to_field_model_map[k].objects.order_by(k)
            select_values['select_' + k] = [ i
                for i in mgr.all().values_list(k, flat=True).distinct() ] 

        return select_values

class DefaultView(GenericAnalyticsView):

    def __call__(self, request):
        context = {}
        context.update(self._getAvailableFormOptions())
        return render(request, self.template_path, context)

class SearchView(GenericAnalyticsView):

    def __call__(self, request):
        context={}
        context.update(self._getAvailableFormOptions())
        context.update(self.__processRequest(request))
        return render(request, self.template_path, context)

    def __gatherSearchOptions(self, request):

        options = {}

        for k in self.key_to_field_model_map:
            options[k] = request.GET.get(k, None)

        for k,v in options.items():
            if v is None or v == '':
                options = None
                break

        return options

    def __grabYoutubeAnalytics(self, opts):
        results = dict()

        for k in opts:
            retQS = self.key_to_field_model_map[k].objects.filter(
                **{k: opts[k]}
            ).order_by('youtube')

            if len(retQS) == 0:
                results = None
                break

            results[k] = retQS

        return results

    def __selectChannels(self, analytics):

        unique_channels_per_analytics_list = [
            {item.youtube.id for item in analytics[k]}
            for k in analytics
        ]

        unique_channel_ids = functools.reduce(lambda a1, a2: a1 & a2,
                                    unique_channels_per_analytics_list)

        for k in analytics:
            analytics[k] = analytics[k].filter(
                youtube__in=unique_channel_ids
            ).order_by('youtube')

        channels = list( sorted(
            [ self.__calculateRating(i)
                     for i in zip(*analytics.values()) # order is not
              # important in our case, should be orderd otherwise
            ],
            key=lambda d: d['weight'],
            reverse=True
        ))

        return channels

    def __calculateRating(self, channel_analytics):
        
        Youtube_model = channel_analytics[0].youtube
        return {
            'youtube': {
                'id': Youtube_model.id,
                'name': Youtube_model.name,
                'title': Youtube_model.title,
            },
            'weight': round(Youtube_model.rank *
                       channel_analytics[0].viewer_percentage *
                       channel_analytics[1].viewer_percentage *
                       channel_analytics[2].viewer_percentage *
                       channel_analytics[3].viewer_percentage,
                       2)
        }

    def __processRequest(self, request):

        opts = self.__gatherSearchOptions(request)

        status = {
            'message': 'No results has been found'
        }

        if opts is not None:
            status['opts']= ["{}: '{}',".format(k, v)
                             for k,v in opts.items()]
            status['message'] = 'Search results'
            analytics = self.__grabYoutubeAnalytics(opts)
            if analytics is not None:
                status['channels'] = self.__selectChannels(analytics) 
        return status

