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

#include <assert.h>
#include <stddef.h>
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

void *sampgdk_plugin_address_to_handle(void *address) {
  MEMORY_BASIC_INFORMATION mbi;

  assert(address != NULL);
  if (VirtualQuery(address, &mbi, sizeof(mbi)) == 0) {
    return NULL;
  }

  return (void*)mbi.AllocationBase;
}

void sampgdk_plugin_address_to_filename(void *address, char *filename,
                                        size_t size) {
  assert(address != NULL);
  assert(filename != NULL);
  GetModuleFileName((HMODULE)sampgdk_plugin_address_to_handle(address),
                    filename, size);
}

void *sampgdk_plugin_find_symbol(void *plugin, const char *name)  {
  assert(plugin != NULL);
  assert(name != NULL);
  return (void*)GetProcAddress((HMODULE)plugin, name);
}
