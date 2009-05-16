from zope.schema.interfaces import ValidationError
from zope.component import getMultiAdapter

from zope.app.form.interfaces import WidgetInputError
from zope.app.form.browser.interfaces import \
    ISourceQueryView, ITerms, IWidgetInputErrorView
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.app.vocabularies.interfaces import IBrowsableTerm

class SliderWidget(SimpleInputWidget):
    
    template = ViewPageTemplateFile('sliderwidget.pt')

    def id(self):
        return self.name.replace('.', '-')

    def action_id(self):
        return self._prefix.replace('.', '')

    def js(self):
        return """
(function($){
$(document).ready(function(){

    $("#%(id)s-slider").slider({
        min:%(min)i,
        max:%(max)i,
        value: %(default)i,
        change: function(e, ui){
            $("#%(id)s-value").attr('value', ui.value);
            $("#%(id)s-slider p").html(String(ui.value));
        }
    });
    
});
})(jQuery);

on('action_button_clicked').do(function(btn){
    if($(btn).attr('name') == '%(action_id)s'){
        $('#%(id)s-slider').slider('moveTo', %(default)i);
    }
});

        """ % {
            'id' : self.id(),
            'min' : self.context.min,
            'max' : self.context.max,
            'default' : self.context.default,
            'action_id' : self.action_id()
        }

    def __call__(self):
        return self.template(self)