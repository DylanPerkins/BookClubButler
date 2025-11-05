from discord_http import commands, Context
import time

from utilities.data import CustomClient
from utilities import strings, permissions


class CreateSprint(commands.Cog):
    def __init__(self, bot: CustomClient):
        self.bot: CustomClient = bot

    server = commands.SubGroup(name="sprint")

    @server.command(name="create", description="Create a new sprint")
    @commands.check(permissions.is_administrator)
    async def create_sprint(self, ctx: Context, name: str, total_chapters: int, split_amount: int):
        """Creates a new sprint with the given parameters."""

        async def call_after():
            # Fetch starting message
            starting_message = strings.strings().starting_message.format(name=name)

            # Create a new channel, in the current category
            category = ctx.channel.parent_id

            sprint_channel = await ctx.guild.create_text_channel(name=name, parent_id=category)

            await sprint_channel.send(content=starting_message)

            # Create public threads for each chapter split
            # Ex. total_chapters = 10, split_amount = 3
            # Creates threads for chapters: 1-3, 4-6, 7-9, 10

            current_chapter = 1

            while current_chapter <= total_chapters:
                # Calculate the end chapter for this thread
                end_chapter = min(current_chapter + split_amount - 1, total_chapters)

                # Create the thread
                thread = await sprint_channel.create_thread(
                    name=strings.strings().thread_title.format(start=current_chapter, end=end_chapter) if current_chapter != end_chapter else strings.strings().thread_title_single.format(chapter=current_chapter),
                    type=11  # Public Thread
                )

                await thread.send(
                    content=strings.strings().thread_description.format(start=current_chapter, end=end_chapter) if current_chapter != end_chapter else strings.strings().thread_description_single.format(chapter=end_chapter)
                )

                current_chapter = end_chapter + 1

                sleep(0.3)  # To avoid rate limits

            await ctx.edit_original_response(
                content=f"✅ Sprint {name} created successfully!",
            )

        return ctx.response.defer(thinking=True, call_after=call_after, ephemeral=True)


def sleep(seconds: float):
    time.sleep(seconds)


async def setup(bot: CustomClient):
    await bot.add_cog(CreateSprint(bot))
    print("Loaded cog: sprint")
