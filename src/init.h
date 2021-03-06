/* Copyright (C) 2013 Zeex
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

#ifndef SAMPGDK_INIT_H_
#define SAMPGDK_INIT_H_

#define DEFINE_INIT_FUNC(f) \
  int sampgdk_##f##_init(void)

#define DEFINE_CLEANUP_FUNC(f) \
  void sampgdk_##f##_cleanup(void)

int  sampgdk_module_init(void);
void sampgdk_module_cleanup(void);

#endif /* !SAMPGDK_INIT_H_ */
