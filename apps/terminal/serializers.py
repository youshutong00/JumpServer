# -*- coding: utf-8 -*-
#

from django.utils import timezone
from rest_framework import serializers

from .models import Terminal, TerminalHeatbeat
from .hands import ProxyLog


class TerminalSerializer(serializers.ModelSerializer):
    proxy_online = serializers.SerializerMethodField()
    is_alive = serializers.SerializerMethodField()

    class Meta:
        model = Terminal
        fields = ['id', 'name', 'ip', 'type', 'url', 'comment',
                  'is_active', 'get_type_display', 'proxy_online', 'is_alive']

    @staticmethod
    def get_proxy_online(obj):
        return ProxyLog.objects.filter(terminal=obj.name, is_finished=False).count()

    @staticmethod
    def get_is_alive(obj):
        log = obj.terminalheatbeat_set.last()
        if timezone.now() - log.date_created > timezone.timedelta(seconds=600):
            return False
        else:
            return True


class TerminalHeatbeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalHeatbeat


if __name__ == '__main__':
    pass
