from spectator.structures import ObservableObject
import wx


class Model(ObservableObject):
    name = 'Joe Blogs'
    email = 'joe.blogs@company.com'
    administrator = True


class DBTextCtrl(wx.TextCtrl):
    def BindToProperty(self, model, property):
        model.observe_property(property, lambda value: wx.CallAfter(self.ChangeValue, value))


class DBCheckBox(wx.CheckBox):
    def BindToProperty(self, model, property):
        model.observe_property(property, lambda value: wx.CallAfter(self.SetValue, bool(value)))


class MyPanel(wx.Panel):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = model
        self.create_controls()

    def create_controls(self):
        name_label = wx.StaticText(self, label='&Name')
        self.name_ctrl = DBTextCtrl(self)
        self.name_ctrl.BindToProperty(self._model, 'name')
        email_label = wx.StaticText(self, label='&Email')
        self.email_ctrl = DBTextCtrl(self)
        self.email_ctrl.BindToProperty(self._model, 'email')
        self.admin_ctrl = DBCheckBox(self, label='&Administrator')
        self.admin_ctrl.BindToProperty(self._model, 'administrator')

        update_button = wx.Button(self, label='&Update values')
        self.Bind(wx.EVT_BUTTON, self.onUpdate, update_button)

    def onUpdate(self, event):
        self._model.name = 'John Smith'
        self._model.email = 'john.smith@microsoft.com'
        self._model.administrator = False
        self.name_ctrl.SetFocus()


class MyFrame(wx.Frame):
    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._model = model
        self._model.observe_property('name', self.update_name)

    def update_name(self, value):
        wx.CallAfter(self.SetTitle, '{0} - Data Binding Example'.format(value))


if __name__ == '__main__':
    app = wx.App()
    model = Model()
    frame = MyFrame(model, parent=None, title='Data Binding Example')
    panel = MyPanel(model, parent=frame)
    frame.Show()
    app.MainLoop()
