/* Copyright (C) 2012-2013 Zeex
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#define _GNU_SOURCE
#include <assert.h>
#include <dlfcn.h>
#include <stddef.h>
#include <string.h>

void *sampgdk_plugin_address_to_handle(void *address) {
  Dl_info info;

  assert(address != NULL);
  if (dladdr(address, &info) == 0) {
    return NULL;
  }

  return dlopen(info.dli_fname, RTLD_NOW);
}

void sampgdk_plugin_address_to_filename(void *address, char *filename,
                                        size_t size) {
  Dl_info info;

  assert(address != NULL);
  assert(filename != NULL);

  if (dladdr(address, &info) == 0) {
    return;
  }

  strncpy(filename, info.dli_fname, size);
}

void *sampgdk_plugin_find_symbol(void *plugin, const char *name)  {
  assert(plugin != NULL);
  assert(name != NULL);
  return dlsym(plugin, name);
}
