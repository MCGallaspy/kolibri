'use strict';
var logging = require('loglevel');
var Mn = require('backbone.marionette');
var _ = require('lodash');

logging.setDefaultLevel(2);

logging.info('Component views loaded!');


var AbstractTextInput = Mn.ItemView.extend({
    template: function(serialized_model) {
        var template_html;
        if (this.model.get('enabled')) {
            template_html = '<input type="' + this.input_tag_type + '" placeholder="Search here!">';
        } else {
            template_html = '<input type="' + this.input_tag_type + '" disabled placeholder="Search here!">';
        }
        return _.template(template_html);
    },

    initialize: function() {
        _.bindAll(this, 'template');
    },

    triggers: {
        'change input': 'inputChanged',
        'focusout input': 'inputChanged'
    },

    events: {
        'keyup input': 'keyup'
    },

    keyup: function(ev) {
        if(ev.which === 13) { // 13 corresponds to enter, and is normalized by jQuery
            this._trigger();
        }
    },

    onInputChanged: function(){
        this._trigger();
    },

    _trigger: function() {
        this.trigger('text_input:text_changed', this.$el.find('input').val());
    },

    clear: function() {
        this.$el.find('input').val('');
    },

    toggleEnabled: function() {
        this.model.set('enabled', !this.model.get('enabled'));
    }
});


var TextLineInput = AbstractTextInput.extend({
    input_tag_type: 'search'
});


var TextAreaInput = AbstractTextInput.extend({
    template: function(serialized_model) {
        var template_html;
        if (this.model.get('enabled')) {
            template_html = '<textarea placeholder="Write here!">';
        } else {
            template_html = '<textarea disabled placeholder="Write here!">';
        }
        return _.template(template_html);
    }
});


var PasswordInput = AbstractTextInput.extend({
    input_tag_type: 'password'
});


var ValidatingTextInput = AbstractTextInput.extend({
    input_tag_type: 'search'
});


/*
Tag is an implementation detail -- not exposed directly, but rather used in TagList.
 */
var Tag = Mn.ItemView.extend({
    template: _.template('<span class="tag"><%= name %></span>'),

    // The triggers hash converts DOM events into Backbone events
    triggers: {
        'click span': 'tagClicked'
    }
});

var TagList = Mn.CollectionView.extend({
    childView: Tag,

    childEvents: {
        tagClicked: 'onChildTagClicked'
    },

    onChildTagClicked: function(child, args) {
        this.trigger('tag_list:tag_clicked', child.model.get('name'));
    }
});


module.exports = {
    TextLineInput: TextLineInput,
    TextAreaInput: TextAreaInput,
    PasswordInput: PasswordInput,
    ValidatingTextInput: ValidatingTextInput,
    TagList: TagList
};
