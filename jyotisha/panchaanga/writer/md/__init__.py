from io import StringIO

from indic_transliteration import sanscript

from jyotisha.panchaanga.writer.md import day_details


def make_md(panchaanga, scripts=None):
  if scripts is None:
    scripts = [sanscript.DEVANAGARI]
  output_stream = StringIO()
  daily_panchaangas = panchaanga.daily_panchaangas_sorted()
  for day_index, daily_panchaanga in enumerate(daily_panchaangas):
    if daily_panchaanga.date < panchaanga.start_date or daily_panchaanga.date > panchaanga.end_date:
      continue
    (title, details) = day_details.day_summary(d=day_index, panchaanga=panchaanga, script=scripts[0])
    print("## %s◢◣%s" % (daily_panchaanga.date.get_date_str(), title), file=output_stream)
    print(details, file=output_stream)

  return output_stream.getvalue()

