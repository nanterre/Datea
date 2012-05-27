from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from datea.datea_image.models import DateaImage 
from datea.datea_subpage.models import DateaSubpage
from datea.datea_category.models import DateaCategory
from mptt.fields import TreeForeignKey, TreeManyToManyField


class DateaReport(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="reports")
    
    # timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    
    # status, published
    published = models.BooleanField(_("published"), default=True)
    status_choices = (
            ('new',_('new')), 
            ('reviewed', _('reviewed')), 
            ('solved', _('solved'))
        )
    status = models.CharField(_("status"), max_length=15, choices=status_choices, default="new")
    
    # content
    content = models.TextField(_("Content"))
    images = models.ManyToManyField(DateaImage, verbose_name=_('Images'), null=True, blank=True, related_name="report_images")
    
    # location
    position = models.PointField(_('Position'), blank=True, null=True, spatial_index=False)
    address = models.CharField(_('Address'), max_length=255, blank=True, null=True)
    
    category = TreeForeignKey(DateaCategory, verbose_name=_("Category"), null=True, blank=True, default=None, related_name="reports")
    
    # stats
    vote_count = models.IntegerField(default=0, blank=True, null=True)
    comment_count = models.IntegerField(default=0,blank=True, null=True)
    follow_count = models.IntegerField(default=0, blank=True, null=True)
    reply_count = models.IntegerField(default=0, blank=True, null=True)
    
    # Object Manager from geodjango
    objects = models.GeoManager()
    
    def __unicode__(self):
        return strip_tags(self.author.username+': '+self.content)[:100]
    
    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')
        
    
        
class DateaReportEnvironment(models.Model):
    
    user = models.ForeignKey(User, verbose_name=_('User'), related_name="report_environments")
    
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=30, help_text=_("A string of text as a short id for use at the url of this map (alphanumeric and dashes only"))
    published = models.BooleanField(_("Published"), default=True)
    
    # timestamps
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    
    # text input fields
    short_description = models.CharField(_("Short description / Slogan"), blank=True, null=True, max_length=140, help_text=_("A short description or slogan (max. 140 characters)."))
    mission = models.TextField(_("Mission / Objectives"), blank=True, null=True, max_length=500, help_text=_("max. 500 characters"))
    information_destiny = models.TextField(_("What happens with the data?"), max_length=500, help_text=_("Who receives the information and what happens with it? (max 500 characters)"))
    long_description = models.TextField(_("Description"), blank=True, null=True, help_text=_("Long description (optional)"))
    report_success_message = models.TextField(_("Report success message"), blank=True, null=True, max_length=140, help_text=_("The message someone sees when succesfully filing a report (max. 140 characters)"))
    
    # ZONES
    #zones = models.ManyToManyField(Zone, blank=True, null=True, default=None)
    
    # CATEGORIES
    categories = TreeManyToManyField(DateaCategory, verbose_name=_("Categories"), blank=True, null=True, default=None, help_text=_("The categories for this environment's reports"))
    
    # Sub-page
    subpage = models.ForeignKey(DateaSubpage, verbose_name=_("Sub-page"), blank=True, null=True, help_text=_("Specify a Sub-page for this Report Environment"))
    
    # GEO:
    center = models.PointField(_("Center"), blank=True, null=True, spatial_index=False)
    boundary = models.PolygonField(_("Boundary"), blank=True, null=True, spatial_index=False)
    
    # Object Manager from geodjango
    objects = models.GeoManager()
            
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Report Environment")
        verbose_name_plural = _("Report Environments")
    
    def save(self, *args, **kwargs):
        if self.center == None and self.boundary != None:
            self.center = self.boundary.centroid
            self.center.srid = self.boundary.get_srid()
        super(DateaReportEnvironment, self).save(*args, **kwargs)
    
    
    


    
    
    
