/*
** Copyright (C) 2009-2010 Martin Gl�ck All rights reserved
** Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
**
** This library is free software; you can redistribute it and/or
** modify it under the terms of the GNU Library General Public
** License as published by the Free Software Foundation; either
** version 2 of the License, or (at your option) any later version.
**
** This library is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
** Library General Public License for more details.
**
** You should have received a copy of the GNU Library General Public
** License along with this library; if not, write to the Free
** Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
** ****************************************************************************
**
**++
** Name
**    model_edit_ui
**
** Purpose
**    Define a jQuery UI widget handling the nested many to many forms
**
** Revision Dates
**    20-Jun-2009 (MG) Creation
**    12-Jul-2009 (MG) Min and Max count's are considered for enable/disable
**                     of add/delete button's
**    20-Aug-2009 (MG) Completer added and completion functions added to
**                     Many2Many
**    21-Aug-2009 (MG) Keyboard shortcuts added
**     2-Feb-2010 (MG) Adopted to GTW framework
**     3-Feb-2010 (MG) Swiched form states from int's to char's
**     3-Feb-2010 (MG) Correct form count on submit
++     5-Feb-2010 (MG) `suffix` option added to auto completion
**     6-Feb-2010 (MG) Completion finished
**     9-Feb-2010 (MG) Alphabetically sorted
**     9-Feb-2010 (MG) Copy/rename functions added, button handling changed
**    10-Feb-2010 (MG) Setup auto completion on inline unlocking
**    ��revision-date�����
**--
*/

(function ($)
{
  var field_no_pat = /-M([\dP]+)-/;
  var form_buttons = [ { name           : "Delete-Recover"
                       , add_to_inline  : "true"
                       , href           : "#delete-recover"
                       , default_state  : 0
                       , states         :
                           [ { name     : "delete"
                             , enabled  : "cur_count > min_count"
                             , icon     : "ui-icon-trash"
                             , callback : "_delete_inline"
                             }
                           , { name     : "recover"
                             , enabled  : "cur_count < max_count"
                             , icon     : "ui-icon-plus"
                             , callback : "_undelete_inline"
                             }
                           ]
                       }
                     , { name           : "Rename"
                       , href           : "#rename"
                       , add_to_inline  : "lid"
                       , default_state  : 0
                       , states         :
                           [ { name     : "unlock"
                             , enabled  : "true"
                             , icon     : "ui-icon-pencil"
                             , callback : "_unlock_inline"
                             }
                           , { name     : "lock"
                             , enabled  : "true"
                             , icon     : "ui-icon-arrowreturnthick-1-w"
                             , callback : "_revert_inline"
                             }
                           ]
                       }
                     , { name           : "Copy"
                       , add_to_inline  : "lid"
                       , href           : "#copy"
                       , enabled        : "cur_count < max_count"
                       , icon           : "ui-icon-copy"
                       , callback       : "_copy_inline"
                       }
                     , { name           : "Add new form"
                       , add_to_inline  : "false"
                       , href           : "#add"
                       , enabled        : "cur_count < max_count"
                       , icon           : "ui-icon-plusthick"
                       , callback       : "_add_new_inline"
                       }
                     ]
  var Many2Many =
    { _create : function ()
      {
          var  self      = this;
          var $legend    = this.element.find ("legend");
          var add_class  = this.option.add_class;
          var $m2m_range = this.element.find ("input.many-2-many-range:first");
          var  m2m_range = $m2m_range.attr   ("value").split (":");
          var  cur_count = parseInt (m2m_range [1]);
          var  max_count = parseInt (m2m_range [2]);
          this._setOption ("$prototype", this.element.find (".m2m-prototype"));
          this._setOption ("$m2m_range", $m2m_range);
          this._setOption ("min_count",  parseInt (m2m_range [0]));
          this._setOption ("cur_count",  cur_count);
          this._setOption ("cur_number", cur_count);
          this._setOption ("max_count",  max_count);
          $legend.prepend
              ( '<a href="#add" class="icon-link">'
              +   '<span class="ui-icon ui-icon-plusthick'
              +     '" title="Add ' + $legend.attr ("title") + '">'
              +     'Add'
              +   '</span>'
              + '</a>'
              );
          /* extract all real forms */
          var $forms = this.element.find
              (".m2m-inline-instance:not(.m2m-prototype)");
          for (var i = 0; i < $forms.length; i++)
          {
              this._add_buttons ($forms.eq (i));
          }
          this.element.parents       ("form").many2manysubmit ();
          this._update_button_states ();
          this.element.find (":input[name$=-_lid_a_state_]").each (function ()
          {
              var $this      = $(this);
              var  lid_state = $this.attr   ("value").split (":");
              var  lid       = lid_state [0];
              var  state     = lid_state [1];
              if (state != "P")
              {
                  if (lid)
                      $(this).parents (".m2m-inline-instance")
                             .find    (":input:not([type=hidden])")
                             .attr    ("disabled", "disabled");
                  else
                  {
                      var no = field_no_pat.exec (this.name) [1];
                      self._setup_auto_complete  (no);
                  }
              }
          });
      }
    , _add_buttons : function ($form)
      {
          var $element   = $form;
          var  first_tag = $form.get (0).tagName.toLowerCase ();
          var $l_a_s     = $form.find  ("input[name$=-_lid_a_state_]");
          var  lid       = $l_a_s.attr ("value").split (":") [0];
          if (first_tag == "tr")
          {
              $temp  = $('<td><span class="width-3-icons"></span></td>');
              $form.append ($temp);
              $element = $temp.find ("span");
          }
          for (var i = 0; i < form_buttons.length; i++)
          {
              var button = form_buttons [i];
              if (eval (button.add_to_inline))
              {
                  var icon   = button.icon;
                  if (button.states)
                      icon = button.states [button.default_state].icon
                  $element.append
                      ( '<a href="' + button.href + '" class="icon-link">'
                      +   '<span class="ui-icon ' + icon + '">'
                      +      button.name
                      +   '</span>'
                      + '</a>'
                      );
              }
          }
      }
    , _add_new_inline : function (evt)
      {
          evt.data._copy_form ();
          evt.preventDefault  ();
      }
    , _auto_complete        : function (evt)
    {
        var data     = {};
        var self     = evt.data.self;
        if (self.options.key_handled)
        {
            evt.preventDefault  ();
            evt.stopPropagation ();
            self._setOption      ("key_handled", false);
            return false
        }
        var comp_opt = evt.data.comp_opt;
        var trigger  = evt.currentTarget.name.split (field_no_pat) [2];
        trigger      = comp_opt.triggers [trigger];
        var fields   = trigger ["fields"];
        var value    = evt.currentTarget.value;
        var id       = comp_opt.prefix + "-comp-list"
        $("#" + id).remove (); /* remove old display */
        if (  (trigger.min_chars != undefined)
           && (value.length      >= trigger.min_chars)
           )
        {
            var no = field_no_pat.exec (evt.currentTarget.name) [1];
            var pf = comp_opt.prefix + "-M" + parseInt (no) + "-";
            for (var i = 0;  i < trigger.fields.length; i++)
            {
                var mfn   = trigger.fields [i];
                var value =  $("[name=" + pf + mfn + "]").attr ("value");
                if (value) data [mfn] = value;
            }
            jQuery.get
              ( comp_opt.list_url
              , data
              , function (data, textStatus)
                {
                    if (textStatus == "success")
                    {
                        var comp_data = { comp_data : comp_data
                                        , input     : evt.currentTarget
                                        };
                        var $auto_complete = $(data).attr ("id", id);
                        if ($auto_complete.find (".completion-id").length)
                        {
                            var $input = $(evt.currentTarget);
                            var  pos   = $input.position ();
                            pos.left += $input.width  ();
                            $("#" + id).remove (); /* remove old display */
                            $input.parent ().append ($auto_complete);
                            $auto_complete.css      (pos)
                                          .children ()
                                          .bind ( "click", function (e)
                              {
                                  self._replace_form
                                    (evt, $(e.currentTarget), comp_opt);
                              })
                                          .hover (function (e)
                              {
                                  $(this).addClass ("ui-state-hover");
                              }, function (e)
                              {
                                  $(this).removeClass ("ui-state-hover");
                              });
                        }
                    }
                }
              )
        }
    }
    , _auto_complete_navigation : function (evt)
    {
        var  self      = evt.data.self;
        var  comp_opt  = evt.data.comp_opt;
        var $comp_list = $("#" + comp_opt.prefix + "-comp-list");
        var  handled   = false;
        if ($comp_list.length)
        {
            var $curr_selected = $comp_list.find     (".ui-state-hover");
            var $all           = $comp_list.children ();
            var  curr_idx      = $all.index          ($curr_selected);
            switch (evt.keyCode)
            {
                case 40 : curr_idx += 1;
                          handled = true;
                          break;
                case 38 : curr_idx -= 1;
                          handled = true;
                          break;
                case 27 : $comp_list.remove ();
                          handled = true;
                          break;
                case  9 :
                case 13 : $comp_list.remove ();
                          $comp_list.remove ();
                          self._replace_form (evt, $curr_selected, comp_opt);
                          handled = true;
                          break;
            }
            if (handled)
            {
                if (curr_idx <  0          ) curr_idx = $all.length - 1;
                if (curr_idx >= $all.length) curr_idx = 0;
                $curr_selected.    removeClass  ("ui-state-hover");
                $all.eq (curr_idx).addClass     ("ui-state-hover");
                evt.preventDefault  ();
                evt.stopPropagation ();
                self._setOption       ("key_handled", true);
                return false;
            }
        }
    }
    , _copy_inline   : function (evt)
      {
          var  self   = evt.data;
          var $source = $(evt.target).parents (".m2m-inline-instance");
          var  $new   = self._copy_form ();
          self._restore_form_state ($new, self._save_form_state ($source));
          $new.find  ("input[name$=-_lid_a_state_]").attr ("value", ":N");
          $new.find  ("input[name$=-instance_state]").attr ("value", "");
          evt.preventDefault  ();
          evt.stopPropagation ();
      }
    , _copy_form     : function ()
      {
          var state = {};
          var $prototype = this.options.$prototype;
          var $new       = $prototype.clone ().removeClass ("m2m-prototype");
          /* now that we have cloned the block, let's change the
          ** name/id/for attributes
          */
          this._setOption ("cur_count", this.options.cur_count + 1);
          var cur_number = this.options.cur_number;
          this._setOption ("cur_number", cur_number + 1);
          var pattern    = /-MP-/;
          var new_no     = "-M" + cur_number + "-";
          var $labels    = $new.find     ("label")
          for (var i = 0; i < $labels.length; i++)
          {
              var $l = $labels.eq (i);
              $l.attr ("for", $l.attr ("for").replace (pattern, new_no));
          }
          var $edit_elements = $new.find (":input");
          var  edit_mod_list = ["id", "name"];
          for (var i = 0; i < $edit_elements.length; i++)
          {
              var $e = $edit_elements.eq (i);
              for (var j = 0; j < edit_mod_list.length; j++)
              {
                  var n = edit_mod_list [j];
                  $e.attr (n, $e.attr (n).replace (pattern, new_no));
              }
          }
          /* we are ready to add the new block at the end */
          this._add_buttons          ($new);
          $prototype.parent          ().append ($new);
          this._update_button_states ();
          this._setup_auto_complete  (cur_number);
          $new.find ("input[name$=-_lid_a_state_]").attr ("value", ":N");
          return $new;
      }
    , _delete_inline : function (evt)
      {
          var self   = evt.data;
          var $proto = self.options.$prototype;
          var $form  = $(evt.target).parents (".m2m-inline-instance");
          if (self._forms_equal ($form, $proto))
          {
              $form.remove ();
          }
          else
          {
              var  button        = form_buttons [0];
              var $link          = $form.find  ("a[href=" + button.href + "]");
              var $button        = $link.find  ("span");
              var $elements      = $form.find  (":input:not([type=hidden])");
              var $l_a_s         = $form.find  ("input[name$=-_lid_a_state_]");
              var  lid           = $l_a_s.attr ("value").split (":") [0];
              $elements.attr        ("disabled","disabled")
                       .addClass    ("ui-state-disabled");
              $button.removeClass   (button.states [0].icon)
                     .addClass      (button.states [1].icon);
              $l_a_s.attr ("value", [lid, "U"].join (":"));
          }
          self._setOption ("cur_count", self.options.cur_count - 1);
          self._update_button_states ();
          evt.preventDefault         ();
          evt.stopPropagation        ();
      }
    , _forms_equal : function ($l, $r)
      {
          /* Returns whether the values of the two forms are equal */
          var $l_value_elements = $l.find ("[value]:not([type=hidden])");
          var $r_value_elements = $r.find ("[value]:not([type=hidden])");
          if ($l_value_elements.length != $r_value_elements.length)
              return false;
          for (var i = 0; i < $l_value_elements.length; i++)
          {
              if (  $l_value_elements.eq (i).attr ("value")
                 != $r_value_elements.eq (i).attr ("value")
                 )
                  return false;
          }
          return true;
      }
    , _replace_form : function (evt, $selected, comp_opt)
    {
        var id = comp_opt.prefix + "-comp-list";
        var pk = $selected.find    (".completion-id").text ();
        var no = field_no_pat.exec (evt.currentTarget.name) [1];
        var pf = comp_opt.prefix + "-M" + parseInt (no) + "-";
        jQuery.getJSON
          ( comp_opt.obj_url, { "lid" : pk}
          , function (data, textStatus)
            {
                $("#" + id).remove ();
                if (textStatus == "success")
                {
                    for (var key in data)
                    {
                        var $field = $("[name=" + pf + key + "]");
                        var tag_name = $field [0].nodeName.toLowerCase ();
                        if (tag_name == "input")
                        {
                            $field.attr ("value", data [key]);
                        }
                        $field.attr ("disabled", "disabled");
                    }
                }
            }
          )
    }
    , _restore_form_state : function ($form, state)
      {
          var $elements = $form.find  (":input");
          var  form_no  = state ["_form_no_"];
          for (var i = 0; i < $elements.length; i++)
          {
              var $e  = $elements.eq (i);
              var key = $e.attr ("name").replace (field_no_pat, form_no);
              $e.attr ("value", state [key]);
          }
      }
    , _revert_inline   : function (evt)
      {
          var self           = evt.data;
          var $form          = $(evt.target).parents (".m2m-inline-instance");
          var  button        = form_buttons [1];
          var $link          = $form.find  ("a[href=" + button.href + "]");
          var $button        = $link.find  ("span");
          var $elements      = $form.find  (":input");
          var $l_a_s         = $form.find  ("input[name$=-_lid_a_state_]");
          var  lid           = $l_a_s.attr ("value").split (":") [0];
          self._restore_form_state   ($form, $form.data ("_state"));
          $elements.attr             ("disabled", "disabled");
          $button.removeClass        (button.states [1].icon)
                 .addClass           (button.states [0].icon);
          self._update_button_states ();
          evt.preventDefault         ();
          evt.stopPropagation        ();
      }
    , _save_form_state      : function ($form)
      {
          var $elements = $form.find (":input");
          var  state    =
            {_form_no_ : field_no_pat.exec ($elements.attr ("name")) [0]};
          for (var i = 0; i < $elements.length; i++)
          {
              var $e = $elements.eq (i);
              state [$e.attr ("name")] = $e.attr ("value");
          }
          return state;
      }
    , _setup_auto_complete  : function (no)
      {
          var $prototype = this.options.$prototype;
          var  comp_opt  = $prototype.data  ("completion");
          if (comp_opt != undefined)
          {
              var  pf    = comp_opt.prefix + "-M" + no + "-";
              for (var field_name in comp_opt.triggers)
              {
                  var real_field_name = pf + field_name;
                  $("[name=" + real_field_name + "]").bind
                      ( "keyup"
                      , {comp_opt : comp_opt, self : this}
                      , this._auto_complete
                      ).bind
                      ( "keypress"
                      , {comp_opt : comp_opt, self : this}
                      , this._auto_complete_navigation
                      );;
              }
          }
      }
    , _undelete_inline : function (evt)
      {
          var self           = evt.data;
          var $proto         = self.options.$prototype;
          var $form          = $(evt.target).parents (".m2m-inline-instance");
          var  button        = form_buttons [0];
          var $link          = $form.find  ("a[href=" + button.href + "]");
          var $button        = $link.find  ("span");
          var $elements      = $form.find  (":input:not([type=hidden])");
          var $l_a_s         = $form.find  ("input[name$=-_lid_a_state_]");
          var  lid           = $l_a_s.attr ("value").split (":") [0];
          var  new_state     = "L";
          if (! lid)
          {
              new_state      = "N";
              $elements.removeAttr ("disabled")
          }
          $elements.removeClass ("ui-state-disabled");
          self._setOption ("cur_count", self.options.cur_count + 1);
          $l_a_s.attr ("value", [lid, new_state].join (":"));
          $button.removeClass  (button.states [1].icon)
                 .addClass     (button.states [0].icon);
          self._update_button_states ();
          evt.preventDefault         ();
          evt.stopPropagation        ();
      }
    , _unlock_inline   : function (evt)
      {
          var self            = evt.data;
          var $form           = $(evt.target).parents (".m2m-inline-instance");
          var  button         = form_buttons [1];
          var $link           = $form.find    ("a[href=" + button.href + "]");
          var $button         = $link.find    ("span");
          var $elements       = $form.find    (":input");
          var  link_prefix    = self.options.link_prefix;
          var name = $form.find  ("input[name$=-_lid_a_state_]").each ( function () {
            var $this         = $(this);
            var lid           = $this.attr ("value").split (":") [0];
            var name          = $this.attr ("name");
            var new_state     = "r"
            if (name.split (field_no_pat) [0] == link_prefix)
            {
                /* this is the state field of the link */
                new_state     = "R";
            }
            $this.attr ("value", [lid, new_state].join (":"));
          }).attr ("name");
          $form.data                 ("_state", self._save_form_state ($form));
          $elements.removeAttr       ("disabled")
          $button.removeClass        (button.states [0].icon)
                 .addClass           (button.states [1].icon);
          self._setup_auto_complete  (field_no_pat.exec (name) [1]);
          self._update_button_states ();
          evt.preventDefault         ();
          evt.stopPropagation        ();
      }
    , _update_button_state  : function ( $this
                                       , cur_count, min_count, max_count
                                       , button, state
                                       )
    {
        var  href    = state.href || button.href;
        var $buttons = $this.find
            ('a[href=' + href + '] .' + state.icon.split (" ") [0])
        /* remove old handlers */
        $buttons.unbind ("click")
        if (eval (state.enabled))
        {
            $buttons.bind   ("click", this, this [state.callback])
                    .parent ().removeClass ("ui-state-disabled");
        }
        else
        {
            $buttons.parent ().addClass ("ui-state-disabled");
        }
    }
    , _update_button_states : function ()
      {
          var $this       = this.element;
          var cur_count   = this.options.cur_count;
          var min_count   = this.options.min_count;
          var max_count   = this.options.max_count;
          for (var i = 0; i < form_buttons.length; i++)
          {
              var button        = form_buttons [i];
              if (button.states)
              {
                  for (var si = 0; si < button.states.length; si++)
                  {
                      this._update_button_state
                          ( $this, cur_count, min_count, max_count
                          , button, button.states [si]
                          );
                  }
              }
              else
              {
                  this._update_button_state
                      ($this, cur_count, min_count, max_count, button, button);
              }
          }
          this.options.$m2m_range.attr
              ("value", [min_count, cur_count, max_count].join (":"));
      }
    }
  $.widget ("ui.many2many", Many2Many);
  $.extend
    ( $.ui.many2many
    , { version                          : "0.2.ui-icon-circle-close"
      , defaults                         :
        { add_class                      : "m2m-add"
        }
      }
    );
  var Completer =
    { _create : function ()
      {
          var options = {};
          for (var key in $.ui.completer.defaults)
            {
              options [key] = this.options [key];
            }
          if (options.standalone)
            {
              var  pf    = options.prefix + "-";
              for (var field_name in options.triggers)
              {
                  var real_field_name = pf + field_name;
                  $("[name=" + real_field_name + "]").bind
                      ( "keyup"
                      , {comp_opt : options, self : this}
                      , this._auto_complete
                      ).bind
                      ( "keypress"
                      , {comp_opt : options, self : this}
                      , this._auto_complete_navigation
                      );
              }
              this.element.parents ("form").many2manysubmit ();
            }
          else
            {
              this.element.find (".m2m-prototype").data ("completion", options);
            }
      }
    , _auto_complete        : function (evt)
      {
        var data     = {};
        var self     = evt.data.self;
        if (self.options.key_handled)
        {
            evt.preventDefault  ();
            evt.stopPropagation ();
            self._setOption      ("key_handled", false);
            return false;
        }
        var comp_opt = evt.data.comp_opt;
        var pf       = comp_opt.prefix + "-";
        var trigger  = evt.currentTarget.name.substr (pf.length);
        trigger      = comp_opt.triggers [trigger];
        var fields   = trigger ["fields"];
        var value    = evt.currentTarget.value;
        var id       = comp_opt.prefix + "-comp-list"
        $("#" + id).remove (); /* remove old display */
        if (  (trigger.min_chars != undefined)
           && (value.length      >= trigger.min_chars)
           )
        {
            for (var i = 0;  i < trigger.fields.length; i++)
            {
                var mfn   = trigger.fields [i];
                var value =  $("[name=" + pf + mfn + "]").attr ("value");
                if (value) data [mfn] = value;
            }
            jQuery.get
              ( comp_opt.list_url
              , data
              , function (data, textStatus)
                {
                    if (textStatus == "success")
                    {
                        var comp_data = { comp_data : comp_data
                                        , input     : evt.currentTarget
                                        };
                        var $auto_complete = $(data).attr ("id", id);
                        if ($auto_complete.find (".completion-id").length)
                        {
                            var $input = $(evt.currentTarget);
                            var  pos   = $input.position ();
                            pos.left += $input.width  ();
                            $("#" + id).remove (); /* remove old display */
                            $input.parent ().append ($auto_complete);
                            $auto_complete.css      (pos)
                                          .children ()
                                          .bind ( "click", function (e)
                              {
                                  self._replace_form
                                    (evt, $(e.currentTarget), comp_opt);
                              })
                                          .hover (function (e)
                              {
                                  $(this).addClass ("ui-state-hover");
                              }, function (e)
                              {
                                  $(this).removeClass ("ui-state-hover");
                              });
                        }
                    }
                }
              )
        }
      }
    , _auto_complete_navigation : function (evt)
      {
        var  self      = evt.data.self;
        var  comp_opt  = evt.data.comp_opt;
        var $comp_list = $("#" + comp_opt.prefix + "-comp-list");
        var  handled   = false;
        if ($comp_list.length)
        {
            var $curr_selected = $comp_list.find     (".ui-state-hover");
            var $all           = $comp_list.children ();
            var  curr_idx      = $all.index          ($curr_selected);
            switch (evt.keyCode)
            {
                case 40 : curr_idx += 1;
                          handled = true;
                          break;
                case 38 : curr_idx -= 1;
                          handled = true;
                          break;
                case 27 : $comp_list.remove ();
                          handled = true;
                          break;
                case  9 :
                case 13 : $comp_list.remove ();
                          $comp_list.remove ();
                          self._replace_form (evt, $curr_selected, comp_opt);
                          handled = true;
                          break;
            }
            if (handled)
            {
                if (curr_idx <  0          ) curr_idx = $all.length - 1;
                if (curr_idx >= $all.length) curr_idx = 0;
                $curr_selected.    removeClass  ("ui-state-hover");
                $all.eq (curr_idx).addClass     ("ui-state-hover");
                evt.preventDefault  ();
                evt.stopPropagation ();
                self._setOption       ("key_handled", true);
                return false;
            }
        }
      }
    , _replace_form : function (evt, $selected, comp_opt)
      {
        var id = comp_opt.prefix + "-comp-list";
        var pk = $selected.find    (".completion-id").text ();
        var pf = comp_opt.prefix + "-";
        jQuery.getJSON
          ( comp_opt.obj_url, { "lid" : pk}
          , function (data, textStatus)
            {
                $("#" + id).remove ();
                if (textStatus == "success")
                {
                    for (var key in data)
                    {
                        var $field = $("[name=" + pf + key + "]");
                        var tag_name = $field [0].nodeName.toLowerCase ();
                        if (tag_name == "input")
                        {
                            $field.attr ("value", data [key]);
                        }
                        $field.attr ("disabled", "disabled");
                    }
                }
            }
          );
      }
    }
  $.widget ("ui.completer", Completer);
  $.extend
    ( $.ui.completer
    , { version                          : "0.1"
      , defaults                         :
        { triggers                       : { "subscriber_number"
                                           : { "min_chars" : 2
                                             , "fields"    :
                                                 [ "country_code"
                                                 , "area_code"
                                                 , "subscriber_number"
                                                 ]
                                             }
                                           }
        , list_url                       : ""
        , obj_url                        : "" // id -> pk, no ->number
        , prefix                         : ""
        , standalone                     : true
        }
      }
    );
  var Many2ManySubmit =
    { _create : function ()
      {
          var pattern    = /M\d+-/;
          var self       = this;
          this.element.bind ("submit", function (evt)
          {
              /* first, let's renumerate the inline-instance's */
              self.element.find (".m2m-inline-form-table").each ( function ()
                  {
                      var $this  = $(this);
                      var  no    = -1; /* the first is the prototype */
                      $this.find (".m2m-inline-instance").each (function ()
                      {
                          var $elements      = $(this).find (":input");
                          var  edit_mod_list = ["id", "name"];
                          var  new_no        = "M" + no + "-";
                          for (var i = 0; i < $elements.length; i++)
                          {
                              var $e = $elements.eq (i);
                              for (var j = 0; j < edit_mod_list.length; j++)
                              {
                                  var n = edit_mod_list [j];
                                  $e.attr
                                    ( n
                                    , $e.attr (n).replace (pattern, new_no)
                                    );
                              }
                          }
                          no = no + 1;
                      });
                      var $m2m_range = $this.find (".many-2-many-range:first");
                      var  m2m_range = $m2m_range.attr ("value").split (":");
                      m2m_range [1]  = no;
                      $m2m_range.attr ("value", m2m_range.join (":"));
                  });
              /* now, let's re-enable all input's so that they are set to the
              ** server
              */
              self.element.find (":input").removeAttr ("disabled");
          }
          );
      }
    };
  $.widget ("ui.many2manysubmit", Many2ManySubmit);
})(jQuery);
