# flake8: noqa
# fmt: off
# mypy: disable-error-code="no-any-return, no-untyped-call, misc, type-arg"
# This file was automatically generated by algokit-client-generator.
# DO NOT MODIFY IT BY HAND.
# requires: algokit-utils@^1.2.0
import base64
import dataclasses
import decimal
import typing
from abc import ABC, abstractmethod

import algokit_utils
import algosdk
from algosdk.v2client import models
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    AtomicTransactionResponse,
    SimulateAtomicTransactionResponse,
    TransactionSigner,
    TransactionWithSigner
)

_APP_SPEC_JSON = r"""{
    "hints": {
        "contract(account,account,uint64,uint64,asset)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "asset_opt_in(asset)void": {
            "call_config": {
                "no_op": "CALL"
            }
        },
        "begin_transfer(asset,account,account,uint64,uint64)void": {
            "call_config": {
                "no_op": "CALL"
            }
        }
    },
    "source": {
        "approval": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudW5pdF90cmFuc2Zlci51bml0X2NvbnRyYWN0LkFzc2V0UHVyY2hhc2UuYXBwcm92YWxfcHJvZ3JhbToKICAgIGludGNibG9jayAxIDAgMTAwMCA0CiAgICBjYWxsc3ViIF9fcHV5YV9hcmM0X3JvdXRlcl9fCiAgICByZXR1cm4KCgovLyBzbWFydF9jb250cmFjdHMudW5pdF90cmFuc2Zlci51bml0X2NvbnRyYWN0LkFzc2V0UHVyY2hhc2UuX19wdXlhX2FyYzRfcm91dGVyX18oKSAtPiB1aW50NjQ6Cl9fcHV5YV9hcmM0X3JvdXRlcl9fOgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBBc3NldFB1cmNoYXNlKEFSQzRDb250cmFjdCk6CiAgICBwcm90byAwIDEKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBfX3B1eWFfYXJjNF9yb3V0ZXJfX19iYXJlX3JvdXRpbmdANwogICAgcHVzaGJ5dGVzcyAweDMyZDUzNDEwIDB4YjZjMmIxNDggMHhjZWRiNjU3MyAvLyBtZXRob2QgImNvbnRyYWN0KGFjY291bnQsYWNjb3VudCx1aW50NjQsdWludDY0LGFzc2V0KXZvaWQiLCBtZXRob2QgImFzc2V0X29wdF9pbihhc3NldCl2b2lkIiwgbWV0aG9kICJiZWdpbl90cmFuc2Zlcihhc3NldCxhY2NvdW50LGFjY291bnQsdWludDY0LHVpbnQ2NCl2b2lkIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggX19wdXlhX2FyYzRfcm91dGVyX19fY29udHJhY3Rfcm91dGVAMiBfX3B1eWFfYXJjNF9yb3V0ZXJfX19hc3NldF9vcHRfaW5fcm91dGVAMyBfX3B1eWFfYXJjNF9yb3V0ZXJfX19iZWdpbl90cmFuc2Zlcl9yb3V0ZUA0CiAgICBpbnRjXzEgLy8gMAogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19jb250cmFjdF9yb3V0ZUAyOgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weToxNAogICAgLy8gQGFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIEFzc2V0UHVyY2hhc2UoQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGJ0b2kKICAgIHR4bmFzIEFjY291bnRzCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAyCiAgICBidG9pCiAgICB0eG5hcyBBY2NvdW50cwogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMwogICAgYnRvaQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgNAogICAgYnRvaQogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgNQogICAgYnRvaQogICAgdHhuYXMgQXNzZXRzCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjE0CiAgICAvLyBAYWJpbWV0aG9kCiAgICBjYWxsc3ViIGNvbnRyYWN0CiAgICBpbnRjXzAgLy8gMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19hc3NldF9vcHRfaW5fcm91dGVAMzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NDMKICAgIC8vIEBhYmltZXRob2QKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBBc3NldFB1cmNoYXNlKEFSQzRDb250cmFjdCk6CiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBidG9pCiAgICB0eG5hcyBBc3NldHMKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NDMKICAgIC8vIEBhYmltZXRob2QKICAgIGNhbGxzdWIgYXNzZXRfb3B0X2luCiAgICBpbnRjXzAgLy8gMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19iZWdpbl90cmFuc2Zlcl9yb3V0ZUA0OgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo1MgogICAgLy8gQGFiaW1ldGhvZAogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjYKICAgIC8vIGNsYXNzIEFzc2V0UHVyY2hhc2UoQVJDNENvbnRyYWN0KToKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDEKICAgIGJ0b2kKICAgIHR4bmFzIEFzc2V0cwogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgogICAgYnRvaQogICAgdHhuYXMgQWNjb3VudHMKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDMKICAgIGJ0b2kKICAgIHR4bmFzIEFjY291bnRzCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyA0CiAgICBidG9pCiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyA1CiAgICBidG9pCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjUyCiAgICAvLyBAYWJpbWV0aG9kCiAgICBjYWxsc3ViIGJlZ2luX3RyYW5zZmVyCiAgICBpbnRjXzAgLy8gMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19iYXJlX3JvdXRpbmdANzoKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NgogICAgLy8gY2xhc3MgQXNzZXRQdXJjaGFzZShBUkM0Q29udHJhY3QpOgogICAgdHhuIE9uQ29tcGxldGlvbgogICAgYm56IF9fcHV5YV9hcmM0X3JvdXRlcl9fX2FmdGVyX2lmX2Vsc2VAMTEKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICAhCiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIGNyZWF0aW5nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0c3ViCgpfX3B1eWFfYXJjNF9yb3V0ZXJfX19hZnRlcl9pZl9lbHNlQDExOgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2CiAgICAvLyBjbGFzcyBBc3NldFB1cmNoYXNlKEFSQzRDb250cmFjdCk6CiAgICBpbnRjXzEgLy8gMAogICAgcmV0c3ViCgoKLy8gc21hcnRfY29udHJhY3RzLnVuaXRfdHJhbnNmZXIudW5pdF9jb250cmFjdC5Bc3NldFB1cmNoYXNlLmNvbnRyYWN0KHNlbGxlcjogYnl0ZXMsIGJ1eWVyOiBieXRlcywgcHJpY2U6IHVpbnQ2NCwgcXR5OiB1aW50NjQsIGFzc2V0OiB1aW50NjQpIC0+IHZvaWQ6CmNvbnRyYWN0OgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weToxNC0xNQogICAgLy8gQGFiaW1ldGhvZAogICAgLy8gZGVmIGNvbnRyYWN0KHNlbGYsIHNlbGxlcjogQWNjb3VudCwgYnV5ZXI6IEFjY291bnQsIHByaWNlOiBVSW50NjQsIHF0eTogVUludDY0LCBhc3NldDogQXNzZXQpIC0+IE5vbmU6CiAgICBwcm90byA1IDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6MTYKICAgIC8vIHNlbGYuc2VsbGVyID0gc2VsbGVyCiAgICBwdXNoYnl0ZXMgInNlbGxlciIKICAgIGZyYW1lX2RpZyAtNQogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6MTcKICAgIC8vIHNlbGYuYnV5ZXIgPSBidXllcgogICAgcHVzaGJ5dGVzICJidXllciIKICAgIGZyYW1lX2RpZyAtNAogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6MTgKICAgIC8vIHNlbGYucHJpY2UgPSBwcmljZQogICAgcHVzaGJ5dGVzICJwcmljZSIKICAgIGZyYW1lX2RpZyAtMwogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6MTkKICAgIC8vIHNlbGYucXR5ID0gcXR5CiAgICBwdXNoYnl0ZXMgInF0eSIKICAgIGZyYW1lX2RpZyAtMgogICAgYXBwX2dsb2JhbF9wdXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6MjAKICAgIC8vIHNlbGYuYXNzZXQgPSBhc3NldAogICAgcHVzaGJ5dGVzICJhc3NldCIKICAgIGZyYW1lX2RpZyAtMQogICAgYXBwX2dsb2JhbF9wdXQKICAgIHJldHN1YgoKCi8vIHNtYXJ0X2NvbnRyYWN0cy51bml0X3RyYW5zZmVyLnVuaXRfY29udHJhY3QuQXNzZXRQdXJjaGFzZS5hc3NldF9vcHRfaW4oYXNzZXQ6IHVpbnQ2NCkgLT4gdm9pZDoKYXNzZXRfb3B0X2luOgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo0My00NAogICAgLy8gQGFiaW1ldGhvZAogICAgLy8gZGVmIGFzc2V0X29wdF9pbihzZWxmLCBhc3NldDogQXNzZXQpIC0+IE5vbmU6CiAgICBwcm90byAxIDAKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NDUtNTAKICAgIC8vIGl0eG4uQXNzZXRUcmFuc2ZlcigKICAgIC8vICAgICBhc3NldF9yZWNlaXZlcj1HbG9iYWwuY3VycmVudF9hcHBsaWNhdGlvbl9hZGRyZXNzLAogICAgLy8gICAgIHhmZXJfYXNzZXQ9YXNzZXQsCiAgICAvLyAgICAgYXNzZXRfYW1vdW50PTAsCiAgICAvLyAgICAgZmVlPTEwMDAsCiAgICAvLyApLnN1Ym1pdCgpCiAgICBpdHhuX2JlZ2luCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjQ2CiAgICAvLyBhc3NldF9yZWNlaXZlcj1HbG9iYWwuY3VycmVudF9hcHBsaWNhdGlvbl9hZGRyZXNzLAogICAgZ2xvYmFsIEN1cnJlbnRBcHBsaWNhdGlvbkFkZHJlc3MKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NDgKICAgIC8vIGFzc2V0X2Ftb3VudD0wLAogICAgaW50Y18xIC8vIDAKICAgIGl0eG5fZmllbGQgQXNzZXRBbW91bnQKICAgIGZyYW1lX2RpZyAtMQogICAgaXR4bl9maWVsZCBYZmVyQXNzZXQKICAgIGl0eG5fZmllbGQgQXNzZXRSZWNlaXZlcgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo0NQogICAgLy8gaXR4bi5Bc3NldFRyYW5zZmVyKAogICAgaW50Y18zIC8vIGF4ZmVyCiAgICBpdHhuX2ZpZWxkIFR5cGVFbnVtCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjQ5CiAgICAvLyBmZWU9MTAwMCwKICAgIGludGNfMiAvLyAxMDAwCiAgICBpdHhuX2ZpZWxkIEZlZQogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo0NS01MAogICAgLy8gaXR4bi5Bc3NldFRyYW5zZmVyKAogICAgLy8gICAgIGFzc2V0X3JlY2VpdmVyPUdsb2JhbC5jdXJyZW50X2FwcGxpY2F0aW9uX2FkZHJlc3MsCiAgICAvLyAgICAgeGZlcl9hc3NldD1hc3NldCwKICAgIC8vICAgICBhc3NldF9hbW91bnQ9MCwKICAgIC8vICAgICBmZWU9MTAwMCwKICAgIC8vICkuc3VibWl0KCkKICAgIGl0eG5fc3VibWl0CiAgICByZXRzdWIKCgovLyBzbWFydF9jb250cmFjdHMudW5pdF90cmFuc2Zlci51bml0X2NvbnRyYWN0LkFzc2V0UHVyY2hhc2UuYmVnaW5fdHJhbnNmZXIoYXNzZXQ6IHVpbnQ2NCwgYnV5ZXI6IGJ5dGVzLCBzZWxsZXI6IGJ5dGVzLCBwcmljZTogdWludDY0LCBxdHk6IHVpbnQ2NCkgLT4gdm9pZDoKYmVnaW5fdHJhbnNmZXI6CiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjUyLTUzCiAgICAvLyBAYWJpbWV0aG9kCiAgICAvLyBkZWYgYmVnaW5fdHJhbnNmZXIoc2VsZiwgYXNzZXQ6IEFzc2V0LCBidXllcjogQWNjb3VudCwgc2VsbGVyOiBBY2NvdW50LCBwcmljZTogVUludDY0LCBxdHk6IFVJbnQ2NCkgLT4gTm9uZToKICAgIHByb3RvIDUgMAogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo1NC01OQogICAgLy8gaXR4bi5Bc3NldFRyYW5zZmVyKAogICAgLy8gICAgIHhmZXJfYXNzZXQgPSBhc3NldCwKICAgIC8vICAgICBhc3NldF9yZWNlaXZlcj1idXllciwKICAgIC8vICAgICBhc3NldF9hbW91bnQ9cXR5LAogICAgLy8gICAgIGZlZT0xMDAwCiAgICAvLyApLnN1Ym1pdCgpCiAgICBpdHhuX2JlZ2luCiAgICBmcmFtZV9kaWcgLTEKICAgIGl0eG5fZmllbGQgQXNzZXRBbW91bnQKICAgIGZyYW1lX2RpZyAtNAogICAgaXR4bl9maWVsZCBBc3NldFJlY2VpdmVyCiAgICBmcmFtZV9kaWcgLTUKICAgIGl0eG5fZmllbGQgWGZlckFzc2V0CiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjU0CiAgICAvLyBpdHhuLkFzc2V0VHJhbnNmZXIoCiAgICBpbnRjXzMgLy8gYXhmZXIKICAgIGl0eG5fZmllbGQgVHlwZUVudW0KICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NTgKICAgIC8vIGZlZT0xMDAwCiAgICBpbnRjXzIgLy8gMTAwMAogICAgaXR4bl9maWVsZCBGZWUKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NTQtNTkKICAgIC8vIGl0eG4uQXNzZXRUcmFuc2ZlcigKICAgIC8vICAgICB4ZmVyX2Fzc2V0ID0gYXNzZXQsCiAgICAvLyAgICAgYXNzZXRfcmVjZWl2ZXI9YnV5ZXIsCiAgICAvLyAgICAgYXNzZXRfYW1vdW50PXF0eSwKICAgIC8vICAgICBmZWU9MTAwMAogICAgLy8gKS5zdWJtaXQoKQogICAgaXR4bl9zdWJtaXQKICAgIC8vIHNtYXJ0X2NvbnRyYWN0cy91bml0X3RyYW5zZmVyL3VuaXRfY29udHJhY3QucHk6NjEtNjUKICAgIC8vIGl0eG4uUGF5bWVudCgKICAgIC8vICAgICByZWNlaXZlcj1zZWxsZXIsCiAgICAvLyAgICAgYW1vdW50PXByaWNlICogcXR5LAogICAgLy8gICAgIGZlZT0xMDAwCiAgICAvLyApLnN1Ym1pdCgpCiAgICBpdHhuX2JlZ2luCiAgICAvLyBzbWFydF9jb250cmFjdHMvdW5pdF90cmFuc2Zlci91bml0X2NvbnRyYWN0LnB5OjYzCiAgICAvLyBhbW91bnQ9cHJpY2UgKiBxdHksCiAgICBmcmFtZV9kaWcgLTIKICAgIGZyYW1lX2RpZyAtMQogICAgKgogICAgaXR4bl9maWVsZCBBbW91bnQKICAgIGZyYW1lX2RpZyAtMwogICAgaXR4bl9maWVsZCBSZWNlaXZlcgogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2MQogICAgLy8gaXR4bi5QYXltZW50KAogICAgaW50Y18wIC8vIHBheQogICAgaXR4bl9maWVsZCBUeXBlRW51bQogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2NAogICAgLy8gZmVlPTEwMDAKICAgIGludGNfMiAvLyAxMDAwCiAgICBpdHhuX2ZpZWxkIEZlZQogICAgLy8gc21hcnRfY29udHJhY3RzL3VuaXRfdHJhbnNmZXIvdW5pdF9jb250cmFjdC5weTo2MS02NQogICAgLy8gaXR4bi5QYXltZW50KAogICAgLy8gICAgIHJlY2VpdmVyPXNlbGxlciwKICAgIC8vICAgICBhbW91bnQ9cHJpY2UgKiBxdHksCiAgICAvLyAgICAgZmVlPTEwMDAKICAgIC8vICkuc3VibWl0KCkKICAgIGl0eG5fc3VibWl0CiAgICByZXRzdWIK",
        "clear": "I3ByYWdtYSB2ZXJzaW9uIDEwCgpzbWFydF9jb250cmFjdHMudW5pdF90cmFuc2Zlci51bml0X2NvbnRyYWN0LkFzc2V0UHVyY2hhc2UuY2xlYXJfc3RhdGVfcHJvZ3JhbToKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4K"
    },
    "state": {
        "global": {
            "num_byte_slices": 2,
            "num_uints": 3
        },
        "local": {
            "num_byte_slices": 0,
            "num_uints": 0
        }
    },
    "schema": {
        "global": {
            "declared": {
                "asset": {
                    "type": "uint64",
                    "key": "asset"
                },
                "buyer": {
                    "type": "bytes",
                    "key": "buyer"
                },
                "price": {
                    "type": "uint64",
                    "key": "price"
                },
                "qty": {
                    "type": "uint64",
                    "key": "qty"
                },
                "seller": {
                    "type": "bytes",
                    "key": "seller"
                }
            },
            "reserved": {}
        },
        "local": {
            "declared": {},
            "reserved": {}
        }
    },
    "contract": {
        "name": "AssetPurchase",
        "methods": [
            {
                "name": "contract",
                "args": [
                    {
                        "type": "account",
                        "name": "seller"
                    },
                    {
                        "type": "account",
                        "name": "buyer"
                    },
                    {
                        "type": "uint64",
                        "name": "price"
                    },
                    {
                        "type": "uint64",
                        "name": "qty"
                    },
                    {
                        "type": "asset",
                        "name": "asset"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "asset_opt_in",
                "args": [
                    {
                        "type": "asset",
                        "name": "asset"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            },
            {
                "name": "begin_transfer",
                "args": [
                    {
                        "type": "asset",
                        "name": "asset"
                    },
                    {
                        "type": "account",
                        "name": "buyer"
                    },
                    {
                        "type": "account",
                        "name": "seller"
                    },
                    {
                        "type": "uint64",
                        "name": "price"
                    },
                    {
                        "type": "uint64",
                        "name": "qty"
                    }
                ],
                "returns": {
                    "type": "void"
                }
            }
        ],
        "networks": {}
    },
    "bare_call_config": {
        "no_op": "CREATE"
    }
}"""
APP_SPEC = algokit_utils.ApplicationSpecification.from_json(_APP_SPEC_JSON)
_TReturn = typing.TypeVar("_TReturn")


class _ArgsBase(ABC, typing.Generic[_TReturn]):
    @staticmethod
    @abstractmethod
    def method() -> str:
        ...


_TArgs = typing.TypeVar("_TArgs", bound=_ArgsBase[typing.Any])


@dataclasses.dataclass(kw_only=True)
class _TArgsHolder(typing.Generic[_TArgs]):
    args: _TArgs


def _filter_none(value: dict | typing.Any) -> dict | typing.Any:
    if isinstance(value, dict):
        return {k: _filter_none(v) for k, v in value.items() if v is not None}
    return value


def _as_dict(data: typing.Any, *, convert_all: bool = True) -> dict[str, typing.Any]:
    if data is None:
        return {}
    if not dataclasses.is_dataclass(data):
        raise TypeError(f"{data} must be a dataclass")
    if convert_all:
        result = dataclasses.asdict(data) # type: ignore[call-overload]
    else:
        result = {f.name: getattr(data, f.name) for f in dataclasses.fields(data)}
    return _filter_none(result)


def _convert_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.TransactionParametersDict:
    return typing.cast(algokit_utils.TransactionParametersDict, _as_dict(transaction_parameters))


def _convert_call_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
) -> algokit_utils.OnCompleteCallParametersDict:
    return typing.cast(algokit_utils.OnCompleteCallParametersDict, _as_dict(transaction_parameters))


def _convert_create_transaction_parameters(
    transaction_parameters: algokit_utils.TransactionParameters | None,
    on_complete: algokit_utils.OnCompleteActionName,
) -> algokit_utils.CreateCallParametersDict:
    result = typing.cast(algokit_utils.CreateCallParametersDict, _as_dict(transaction_parameters))
    on_complete_enum = on_complete.replace("_", " ").title().replace(" ", "") + "OC"
    result["on_complete"] = getattr(algosdk.transaction.OnComplete, on_complete_enum)
    return result


def _convert_deploy_args(
    deploy_args: algokit_utils.DeployCallArgs | None,
) -> algokit_utils.ABICreateCallArgsDict | None:
    if deploy_args is None:
        return None

    deploy_args_dict = typing.cast(algokit_utils.ABICreateCallArgsDict, _as_dict(deploy_args))
    if isinstance(deploy_args, _TArgsHolder):
        deploy_args_dict["args"] = _as_dict(deploy_args.args)
        deploy_args_dict["method"] = deploy_args.args.method()

    return deploy_args_dict


@dataclasses.dataclass(kw_only=True)
class ContractArgs(_ArgsBase[None]):
    seller: str | bytes
    buyer: str | bytes
    price: int
    qty: int
    asset: int

    @staticmethod
    def method() -> str:
        return "contract(account,account,uint64,uint64,asset)void"


@dataclasses.dataclass(kw_only=True)
class AssetOptInArgs(_ArgsBase[None]):
    asset: int

    @staticmethod
    def method() -> str:
        return "asset_opt_in(asset)void"


@dataclasses.dataclass(kw_only=True)
class BeginTransferArgs(_ArgsBase[None]):
    asset: int
    buyer: str | bytes
    seller: str | bytes
    price: int
    qty: int

    @staticmethod
    def method() -> str:
        return "begin_transfer(asset,account,account,uint64,uint64)void"


class ByteReader:
    def __init__(self, data: bytes):
        self._data = data

    @property
    def as_bytes(self) -> bytes:
        return self._data

    @property
    def as_str(self) -> str:
        return self._data.decode("utf8")

    @property
    def as_base64(self) -> str:
        return base64.b64encode(self._data).decode("utf8")

    @property
    def as_hex(self) -> str:
        return self._data.hex()


class GlobalState:
    def __init__(self, data: dict[bytes, bytes | int]):
        self.asset = typing.cast(int, data.get(b"asset"))
        self.buyer = ByteReader(typing.cast(bytes, data.get(b"buyer")))
        self.price = typing.cast(int, data.get(b"price"))
        self.qty = typing.cast(int, data.get(b"qty"))
        self.seller = ByteReader(typing.cast(bytes, data.get(b"seller")))


@dataclasses.dataclass(kw_only=True)
class SimulateOptions:
    allow_more_logs: bool = dataclasses.field(default=False)
    allow_empty_signatures: bool = dataclasses.field(default=False)
    extra_opcode_budget: int = dataclasses.field(default=0)
    exec_trace_config: models.SimulateTraceConfig | None         = dataclasses.field(default=None)


class Composer:

    def __init__(self, app_client: algokit_utils.ApplicationClient, atc: AtomicTransactionComposer):
        self.app_client = app_client
        self.atc = atc

    def build(self) -> AtomicTransactionComposer:
        return self.atc

    def simulate(self, options: SimulateOptions | None = None) -> SimulateAtomicTransactionResponse:
        request = models.SimulateRequest(
            allow_more_logs=options.allow_more_logs,
            allow_empty_signatures=options.allow_empty_signatures,
            extra_opcode_budget=options.extra_opcode_budget,
            exec_trace_config=options.exec_trace_config,
            txn_groups=[]
        ) if options else None
        result = self.atc.simulate(self.app_client.algod_client, request)
        return result

    def execute(self) -> AtomicTransactionResponse:
        return self.app_client.execute_atc(self.atc)

    def contract(
        self,
        *,
        seller: str | bytes,
        buyer: str | bytes,
        price: int,
        qty: int,
        asset: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `contract(account,account,uint64,uint64,asset)void` ABI method
        
        :param str | bytes seller: The `seller` ABI parameter
        :param str | bytes buyer: The `buyer` ABI parameter
        :param int price: The `price` ABI parameter
        :param int qty: The `qty` ABI parameter
        :param int asset: The `asset` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = ContractArgs(
            seller=seller,
            buyer=buyer,
            price=price,
            qty=qty,
            asset=asset,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def asset_opt_in(
        self,
        *,
        asset: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `asset_opt_in(asset)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = AssetOptInArgs(
            asset=asset,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def begin_transfer(
        self,
        *,
        asset: int,
        buyer: str | bytes,
        seller: str | bytes,
        price: int,
        qty: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to `begin_transfer(asset,account,account,uint64,uint64)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param str | bytes buyer: The `buyer` ABI parameter
        :param str | bytes seller: The `seller` ABI parameter
        :param int price: The `price` ABI parameter
        :param int qty: The `qty` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        args = BeginTransferArgs(
            asset=asset,
            buyer=buyer,
            seller=seller,
            price=price,
            qty=qty,
        )
        self.app_client.compose_call(
            self.atc,
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return self

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> "Composer":
        """Adds a call to create an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns Composer: This Composer instance"""

        self.app_client.compose_create(
            self.atc,
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return self

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> "Composer":
        """Adds a call to the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass"""
    
        self.app_client.compose_clear_state(self.atc, _convert_transaction_parameters(transaction_parameters), app_args)
        return self


class AssetPurchaseClient:
    """A class for interacting with the AssetPurchase app providing high productivity and
    strongly typed methods to deploy and call the app"""

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        ...

    def __init__(
        self,
        algod_client: algosdk.v2client.algod.AlgodClient,
        *,
        creator: str | algokit_utils.Account | None = None,
        indexer_client: algosdk.v2client.indexer.IndexerClient | None = None,
        existing_deployments: algokit_utils.AppLookup | None = None,
        app_id: int = 0,
        signer: TransactionSigner | algokit_utils.Account | None = None,
        sender: str | None = None,
        suggested_params: algosdk.transaction.SuggestedParams | None = None,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        app_name: str | None = None,
    ) -> None:
        """
        AssetPurchaseClient can be created with an app_id to interact with an existing application, alternatively
        it can be created with a creator and indexer_client specified to find existing applications by name and creator.
        
        :param AlgodClient algod_client: AlgoSDK algod client
        :param int app_id: The app_id of an existing application, to instead find the application by creator and name
        use the creator and indexer_client parameters
        :param str | Account creator: The address or Account of the app creator to resolve the app_id
        :param IndexerClient indexer_client: AlgoSDK indexer client, only required if deploying or finding app_id by
        creator and app name
        :param AppLookup existing_deployments:
        :param TransactionSigner | Account signer: Account or signer to use to sign transactions, if not specified and
        creator was passed as an Account will use that.
        :param str sender: Address to use as the sender for all transactions, will use the address associated with the
        signer if not specified.
        :param TemplateValueMapping template_values: Values to use for TMPL_* template variables, dictionary keys should
        *NOT* include the TMPL_ prefix
        :param str | None app_name: Name of application to use when deploying, defaults to name defined on the
        Application Specification
            """

        self.app_spec = APP_SPEC
        
        # calling full __init__ signature, so ignoring mypy warning about overloads
        self.app_client = algokit_utils.ApplicationClient(  # type: ignore[call-overload, misc]
            algod_client=algod_client,
            app_spec=self.app_spec,
            app_id=app_id,
            creator=creator,
            indexer_client=indexer_client,
            existing_deployments=existing_deployments,
            signer=signer,
            sender=sender,
            suggested_params=suggested_params,
            template_values=template_values,
            app_name=app_name,
        )

    @property
    def algod_client(self) -> algosdk.v2client.algod.AlgodClient:
        return self.app_client.algod_client

    @property
    def app_id(self) -> int:
        return self.app_client.app_id

    @app_id.setter
    def app_id(self, value: int) -> None:
        self.app_client.app_id = value

    @property
    def app_address(self) -> str:
        return self.app_client.app_address

    @property
    def sender(self) -> str | None:
        return self.app_client.sender

    @sender.setter
    def sender(self, value: str) -> None:
        self.app_client.sender = value

    @property
    def signer(self) -> TransactionSigner | None:
        return self.app_client.signer

    @signer.setter
    def signer(self, value: TransactionSigner) -> None:
        self.app_client.signer = value

    @property
    def suggested_params(self) -> algosdk.transaction.SuggestedParams | None:
        return self.app_client.suggested_params

    @suggested_params.setter
    def suggested_params(self, value: algosdk.transaction.SuggestedParams | None) -> None:
        self.app_client.suggested_params = value

    def get_global_state(self) -> GlobalState:
        """Returns the application's global state wrapped in a strongly typed class with options to format the stored value"""

        state = typing.cast(dict[bytes, bytes | int], self.app_client.get_global_state(raw=True))
        return GlobalState(state)

    def contract(
        self,
        *,
        seller: str | bytes,
        buyer: str | bytes,
        price: int,
        qty: int,
        asset: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `contract(account,account,uint64,uint64,asset)void` ABI method
        
        :param str | bytes seller: The `seller` ABI parameter
        :param str | bytes buyer: The `buyer` ABI parameter
        :param int price: The `price` ABI parameter
        :param int qty: The `qty` ABI parameter
        :param int asset: The `asset` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = ContractArgs(
            seller=seller,
            buyer=buyer,
            price=price,
            qty=qty,
            asset=asset,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def asset_opt_in(
        self,
        *,
        asset: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `asset_opt_in(asset)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = AssetOptInArgs(
            asset=asset,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def begin_transfer(
        self,
        *,
        asset: int,
        buyer: str | bytes,
        seller: str | bytes,
        price: int,
        qty: int,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
    ) -> algokit_utils.ABITransactionResponse[None]:
        """Calls `begin_transfer(asset,account,account,uint64,uint64)void` ABI method
        
        :param int asset: The `asset` ABI parameter
        :param str | bytes buyer: The `buyer` ABI parameter
        :param str | bytes seller: The `seller` ABI parameter
        :param int price: The `price` ABI parameter
        :param int qty: The `qty` ABI parameter
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.ABITransactionResponse[None]: The result of the transaction"""

        args = BeginTransferArgs(
            asset=asset,
            buyer=buyer,
            seller=seller,
            price=price,
            qty=qty,
        )
        result = self.app_client.call(
            call_abi_method=args.method(),
            transaction_parameters=_convert_call_transaction_parameters(transaction_parameters),
            **_as_dict(args, convert_all=True),
        )
        return result

    def create_bare(
        self,
        *,
        on_complete: typing.Literal["no_op"] = "no_op",
        transaction_parameters: algokit_utils.CreateTransactionParameters | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Creates an application using the no_op bare method
        
        :param typing.Literal[no_op] on_complete: On completion type to use
        :param algokit_utils.CreateTransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :returns algokit_utils.TransactionResponse: The result of the transaction"""

        result = self.app_client.create(
            call_abi_method=False,
            transaction_parameters=_convert_create_transaction_parameters(transaction_parameters, on_complete),
        )
        return result

    def clear_state(
        self,
        transaction_parameters: algokit_utils.TransactionParameters | None = None,
        app_args: list[bytes] | None = None,
    ) -> algokit_utils.TransactionResponse:
        """Calls the application with on completion set to ClearState
    
        :param algokit_utils.TransactionParameters transaction_parameters: (optional) Additional transaction parameters
        :param list[bytes] | None app_args: (optional) Application args to pass
        :returns algokit_utils.TransactionResponse: The result of the transaction"""
    
        return self.app_client.clear_state(_convert_transaction_parameters(transaction_parameters), app_args)

    def deploy(
        self,
        version: str | None = None,
        *,
        signer: TransactionSigner | None = None,
        sender: str | None = None,
        allow_update: bool | None = None,
        allow_delete: bool | None = None,
        on_update: algokit_utils.OnUpdate = algokit_utils.OnUpdate.Fail,
        on_schema_break: algokit_utils.OnSchemaBreak = algokit_utils.OnSchemaBreak.Fail,
        template_values: algokit_utils.TemplateValueMapping | None = None,
        create_args: algokit_utils.DeployCallArgs | None = None,
        update_args: algokit_utils.DeployCallArgs | None = None,
        delete_args: algokit_utils.DeployCallArgs | None = None,
    ) -> algokit_utils.DeployResponse:
        """Deploy an application and update client to reference it.
        
        Idempotently deploy (create, update/delete if changed) an app against the given name via the given creator
        account, including deploy-time template placeholder substitutions.
        To understand the architecture decisions behind this functionality please see
        <https://github.com/algorandfoundation/algokit-cli/blob/main/docs/architecture-decisions/2023-01-12_smart-contract-deployment.md>
        
        ```{note}
        If there is a breaking state schema change to an existing app (and `on_schema_break` is set to
        'ReplaceApp' the existing app will be deleted and re-created.
        ```
        
        ```{note}
        If there is an update (different TEAL code) to an existing app (and `on_update` is set to 'ReplaceApp')
        the existing app will be deleted and re-created.
        ```
        
        :param str version: version to use when creating or updating app, if None version will be auto incremented
        :param algosdk.atomic_transaction_composer.TransactionSigner signer: signer to use when deploying app
        , if None uses self.signer
        :param str sender: sender address to use when deploying app, if None uses self.sender
        :param bool allow_delete: Used to set the `TMPL_DELETABLE` template variable to conditionally control if an app
        can be deleted
        :param bool allow_update: Used to set the `TMPL_UPDATABLE` template variable to conditionally control if an app
        can be updated
        :param OnUpdate on_update: Determines what action to take if an application update is required
        :param OnSchemaBreak on_schema_break: Determines what action to take if an application schema requirements
        has increased beyond the current allocation
        :param dict[str, int|str|bytes] template_values: Values to use for `TMPL_*` template variables, dictionary keys
        should *NOT* include the TMPL_ prefix
        :param algokit_utils.DeployCallArgs | None create_args: Arguments used when creating an application
        :param algokit_utils.DeployCallArgs | None update_args: Arguments used when updating an application
        :param algokit_utils.DeployCallArgs | None delete_args: Arguments used when deleting an application
        :return DeployResponse: details action taken and relevant transactions
        :raises DeploymentError: If the deployment failed"""

        return self.app_client.deploy(
            version,
            signer=signer,
            sender=sender,
            allow_update=allow_update,
            allow_delete=allow_delete,
            on_update=on_update,
            on_schema_break=on_schema_break,
            template_values=template_values,
            create_args=_convert_deploy_args(create_args),
            update_args=_convert_deploy_args(update_args),
            delete_args=_convert_deploy_args(delete_args),
        )

    def compose(self, atc: AtomicTransactionComposer | None = None) -> Composer:
        return Composer(self.app_client, atc or AtomicTransactionComposer())
