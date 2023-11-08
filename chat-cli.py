#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
from collections import defaultdict
from os import environ

import openai
from dotenv import load_dotenv
from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]

with open("pricing.json") as f:
    pricing = json.load(f)

messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. You help the user accomplish their tasks efficiently.",
    }
]

token_counter = defaultdict(int)


def calculate_total_cost(token_counter, model, pricing):
    return sum(
        (count / 1000) * pricing[model][token_type]
        for token_type, count in token_counter.items()
    )


def get_chat_response(message, messages, token_counter, **kwargs):
    msg = {"role": "user", "content": message}
    messages += [msg]
    completion = openai.ChatCompletion.create(
        model=kwargs["model"], temperature=kwargs["temperature"], messages=messages
    )
    # update token_counter
    token_counter["prompt_tokens"] += completion.usage.prompt_tokens
    token_counter["completion_tokens"] += completion.usage.completion_tokens
    messages += [completion.choices[0].message]
    return messages[-1]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", type=str, default="gpt-3.5-turbo", choices=pricing.keys())
    p.add_argument("--temperature", type=float, default=1.0)
    args = p.parse_args()

    # convert args to mapping
    args = vars(args)
    console = Console()

    # chat loop
    while True:
        rprint("[bold green]User:[/]")
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            break
        rprint("[bold blue]Assistant:[/] [italic]thinking...[/]")
        response = get_chat_response(user_input, messages, token_counter, **args)
        print("\033[A\033[K", end="")
        rprint(f"[bold red]{response['role'].capitalize()}:[/]")
        console.print(Markdown(response["content"]))

    cost = calculate_total_cost(token_counter, args["model"], pricing)
    rprint(f"[bold blue]Total cost of conversation:[/] $ {cost:.2f}")
