import gettext


class _(str):

    observers = set()
    lang = None

    def __new__(cls, s):
        dic = [('Bitcoin', 'VIPSTARCOIN'), ('Bitcoins', 'VIPSTARCOINs'), ('bitcoin', 'vipstarcoin'), ('bitcoins', 'vipstarcoins'), ('mBTC/kB', 'mVIPS/kB'), ('ビットコイン', 'ビップスターコイン')]
        for b, m in dic:
            s = s.replace(m, b)
        if _.lang is None:
            _.switch_lang('en')
        t = _.translate(s)
        for b, m in dic:
            t = t.replace(b, m)
        o = super(_, cls).__new__(cls, t)
        o.source_text = s
        return o

    @staticmethod
    def translate(s, *args, **kwargs):
        return _.lang(s)

    @staticmethod
    def bind(label):
        try:
            _.observers.add(label)
        except:
            pass
        # garbage collection
        new = set()
        for label in _.observers:
            try:
                new.add(label)
            except:
                pass
        _.observers = new

    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        from electrum.i18n import LOCALE_DIR
        locales = gettext.translation('electrum', LOCALE_DIR, languages=[lang], fallback=True)
        _.lang = locales.gettext
        for label in _.observers:
            try:
                label.text = _(label.text.source_text)
            except:
                pass
