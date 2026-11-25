# 条件分工与交接

仅在实际分工时读取。先按真实来源建立素材清单，核对重复链接、连续片段、关联状态与跨姿态证据；文件数量和视频分钟数不等于独立任务数量。默认由主智能体按完整业务流程连续执行，下载、抽帧、hash 和拼图可用脚本并发。单智能体不建立 delegation-plan 或 handoff 文件。

多份录屏／业务流程可以独立处理且收益明确时，默认最多 2 个子智能体，按完整录屏或业务流程分派；必要时也可在完整受审清单冻结后按独立页面组分派。关联滚动、弹层对照和跨姿态依据放同一任务，不按每几张图创建执行者。单份复杂材料如需独立复核，可在全页巡检完成后委托重点复查；严格双轮才另建全量第二轮任务。不建立多层质量／预审／修补队列。

在工具与当前授权允许时使用分工；用户要求单智能体时遵从，工具不可用时主智能体执行并如实说明。skill 是任务说明，安装本身不会后台启动 AI。首选独立上下文，只传必要用户事实、原始证据索引、路径／hash、阶段、规则版本、判定范围／例外、读图预算和完成标准；不默认继承完整图片历史。子任务读取本平台 skill，混合平台材料分开处理，不能扩展判错权限、动态测试或自行发布。

主智能体从实际完整清单建立分阶段 manifest，phase 为 capture、review 或 recheck；capture 的单位是录屏／关联素材组，review 的单位是完整受审状态或页面组，默认 recheck 仅分配问题／疑点。expected_units 不能照抄子任务自报范围。同阶段分配无重叠且覆盖全部所需单元；每个任务在独立 output_dir 写结果，禁止改主 capture／review 文件或其他任务输出。聊天只交接路径、完成／待处理范围、新发现和必要证据摘要，图片和大 JSON 留在文件中。

manifest 使用 scripts/validate_handoffs.py 的现有契约：schema_version=1、phase、rule_version、expected_units、evidence（ID 对应 path 与 sha256）和 tasks（id、units、evidence_ids、output_dir）。每个任务的证据清单覆盖其所有必要材料。

~~~json
{"schema_version":1,"phase":"review","rule_version":"本平台实际规则版本","expected_units":["P1"],"evidence":{"E1":{"path":"evidence/p1.png","sha256":"实际hash"}},"tasks":[{"id":"worker1","units":["P1"],"evidence_ids":["E1"],"output_dir":"tasks/worker1"}]}
~~~

每个任务在其 output_dir 写 handoff.json：task_id、phase、rule_version、status（complete/incomplete）、completed_units、pending_units、evidence_hashes 和 result_files（相对任务目录的 path 与 sha256）。至少包含真实阶段结果文件；未执行的范围列 pending_units，不写 complete。正式检查记录仍采用本平台 schema。

~~~bash
python3 scripts/validate_handoffs.py MANIFEST --plan-only
# 主智能体核对清单后分派；全部结果到位后：
python3 scripts/validate_handoffs.py MANIFEST
~~~

ready_for_merge=true 只证明身份、覆盖、独立目录、版本与 hash 一致，不证明截图识别和审查正确。主智能体核对真实状态／组件记录、遗漏、重复与分歧；有分歧回到原图、适用条件和官方依据，不投票。缺口、共享文件、重复单元、证据改变或版本不符时停止合并，修复后接续。任务变更只传受影响约束，并确认执行者收到；交接频繁或重复读图增多时收回相关分工。

两端均可用本平台 workflow.py merge RUN CAPTURE... 合并完整采集；安卓继续 prepare／seed，苹果在真实目标到位后 init／seed。合并保留唯一 ID、原采集文件、来源 hash 与原图路径；不能混用平台 schema。缺输出目标时可以先采集到本地，不造 target。采集质量与全页巡检按 batch-execution.md 执行，不因子任务已完成就省略主清单对账。

每个实际上下文使用自己的累计读图账本；子任务仍执行 check／record／fail。工具并发不增加一次可读图量；新任务名或继承历史的分叉不重置上下文。中断保留待处理范围和检查点，不能用创建子任务绕过主上下文预算。最终报告编号、归并、外部写入和发布回读由主智能体负责。
