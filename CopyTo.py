import sublime, sublime_plugin
import re

class CopyToCommand(sublime_plugin.WindowCommand):
  def run(self, input_string=""):
    self.run_setup()
    self.show_copyto_input(input_string)

  def run_setup(self):
    self.view = self.window.active_view()

  def show_copyto_input(self, initial):
    self.copyto_view = self.window.show_input_panel('Enter the source lines, the command and the target line (1,2c3)',
      initial, self.on_done, None, None )

  def on_done(self, input_string):
    if len(input_string) != 0:
      self.window.active_view().run_command("copy_to_text", {"input_string": input_string} )


class CopyToTextCommand(sublime_plugin.TextCommand):

  def run(self, edit, input_string):
    match = re.match('^(\d+)(?:,(\d+))?(c|t|m)(\d+)', input_string)
    if match:
      begin = int(match.group(1)) -  1
      end = begin
      if match.group(2) is not None:
        end = int(match.group(2)) - 1
      to = int(match.group(4)) - 1

      move = False
      if match.group(3) == "m":
        move = True

      source_region = self.getRegion(self.view, begin, end)
      line_contents = self.view.substr(source_region)

      insert_point = self.view.text_point(to, 0)
      self.view.insert(edit, insert_point, line_contents)

      if move:
        self.view.erase(edit, source_region)

  def getRegion(self, view, start, end):
    lineFrom = view.full_line(view.text_point(start, 0))
    lineTo = view.full_line(view.text_point(end, 0))

    return sublime.Region(lineFrom.a, lineTo.b)
