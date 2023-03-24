'''
BACKUP ALL DATA

async def __handler_run_wait_for(self, filepath, filename, extension):
    try:
        text = await asyncio.wait_for(self.mask_dict[extension](filepath, filename), timeout=self.time_processing)
        self.default_log.info(f'successful transcoding: {filepath}')
    except asyncio.TimeoutError:
        self.default_log.error(f'transcoding timeout: {filepath}')
        return None
    except UnicodeDecodeError:
        self.default_log.error(f'unicode error: {filepath}')
        return None
    text = await asyncio.wait([self.mask_dict[extension](filepath, filename)], timeout=self.time_processing)
    return text

    @staticmethod
    def copy_files(self, copy_from, copy_to):
        mask = ['doc', 'docx']
        for root, dirs, files in os.walk(copy_from):
            for filename in files:
                extension = filename.split('.')[-1]
                try:
                    mask.index(extension)
                except ValueError:
                    continue
                name = self.__delete_extension(filename)
                if not self.__firebird_base.IsProcessed(name):
                    file_in = "{}/{}".format(root, filename)
                    file_out = "{}/{}".format(copy_to, filename)
                    copyfile(file_in, file_out)
        pass

    def _thread_start(self, filenames, folder, thread_id):
        pulleti_processor_copy = copy.copy(self.pulleti_processor)
        while len(self.file_list):
            filename = filenames.pop(-1)
            extension = filename.split('.')[-1]
            if extension not in self.mask_dict.keys(): continue
            processed_file = ProcessedFile(filename=filename, path=f'{folder}/{filename}')
            doc_handler_log.info(f'Thread: {thread_id}: processed file {processed_file.path}')
            if self.check_processed_file(processed_file.filename): continue
            file_text = self.handler_get_text(processed_file.path, processed_file.filename, extension, thread_id)
            self.handler_output_file(filename, file_text, self.db, processed_file.path, pulleti_processor_copy,
                                     thread_id)

    while len(self.file_list) > 1000:
                time.sleep(self.time_processing)
            for file in files:
                self.file_list.append((folder, file))
        for thread in threads:
            thread.join()

    def handler_get_text(self, filepath, filename, extension, thread_id):
        pool = ThreadPool(processes=1)
        try:
            handler_func = self.mask_dict[extension]
            doc_handler_log.info(f'Thread {thread_id}: {handler_func.__name__} {filepath}')
            async_result = pool.apply_async(handler_func, (filepath, filename))
            text = async_result.get(self.time_processing)
            doc_handler_log.info(f'Thread {thread_id}: success transcoding {filepath}')
            return text
        except multiprocessing.context.TimeoutError:
            doc_handler_log.error(f'Thread {thread_id}: Transcoding timeout: {filepath}')
            pool.close()
            pool.join()
            return None
        except UnicodeDecodeError:
            doc_handler_log.error(f'Thread {thread_id}: Unicode error: {filepath}')
            pool.close()
            pool.join()
            return None
        except Exception as e:
            doc_handler_log.error(f'Thread {thread_id}: Unexpected {e}: {filepath}')
            pool.close()
            pool.join()
            return None

    def handler_get_text(self, filepath, filename, extension):
        text = None
        try:
            with ThreadPool(processes=1) as pool:
                handler_func = self.mask_dict[extension]
                doc_handler_log.info(f'{handler_func.__name__} {filepath}')
                async_result = pool.apply_async(handler_func, (filepath, filename))
                text = async_result.get(self.time_processing)
                doc_handler_log.info(f'success transcoding {filepath}')
            return text
        except multiprocessing.context.TimeoutError:
            doc_handler_log.error(f'transcoding timeout: {filepath}')
        except UnicodeDecodeError:
            doc_handler_log.error(f'unicode error: {filepath}')
        except Exception as e:
            doc_handler_log.error(f'unexpected {e}: {filepath}')
        finally:
            return text

    @doc_handler_log.catch
    def _thread_start(self, filename, folder):
        #pulleti_processor_copy = copy.copy(self.pulleti_processor)
        extension = filename.split('.')[-1]
        if extension not in self.mask_dict.keys(): return
        processed_file = ProcessedFile(filename=filename, path=f'{folder}/{filename}')
        doc_handler_log.info(f'processed file {processed_file.path}')
        if self.check_processed_file(processed_file.filename): return
        file_text = self.handler_get_text(processed_file.path, processed_file.filename, extension)
        self.handler_output_file(filename, file_text, self.db, processed_file.path, self.pulleti_processor)
        doc_handler_log.info(f'processing completed {processed_file.path}')

    def retrieving_numbers_information(self, number_list, limit, offset=0):
        phone_view_list = list()
        session = self.session_master()
        query_number = session.query(TELEPHONES.number, PARAGRAPH.text, DOCUMENTS.path2doc).join(
            TELEPHONES.paragraph).join(
            PARAGRAPH.document).filter(or_(*
                                           [TELEPHONES.number.like(f'%{number}%') for number in number_list])).order_by(
            TELEPHONES.id.desc()).limit(limit).offset(offset).all()
        for phone, paragraph_text, path2doc in query_number:
            phone_view_list.append(PhoneView(phone, paragraph_text, path2doc))
        record_count = session.query(TELEPHONES.number, PARAGRAPH.text, DOCUMENTS.path2doc).join(
            TELEPHONES.paragraph).join(
            PARAGRAPH.document).filter(or_(*
                                           [TELEPHONES.number.like(f'%{number}%') for number in number_list])).count()
        session.close()
        return phone_view_list, record_count

        with CustomProcess(process_count, time_processing=self.time_processing) as pool:
    for folder, subdir, files in os.walk(self.input_dir):
        for file in files:
            if pool.wait_task_limit(TASK_LIMIT):
                pool.apply_async(self.retraining_proj_process,
                                 args=(file, folder, kwargs))
    pool.join()


    def handler_libreoffice(self, filepath, filename):
        file_out = self.__delete_extension(filename)
        file_out += ".txt"
        convert_string = """{} "{}" --outdir {}""".format(CONVERT_DOC2TXT, filepath,
                                                          self.output_dir)
        doc_handler_log.info(convert_string)
        process = subprocess.Popen(convert_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   preexec_fn=os.setsid)
        try:
            process.wait(self.time_processing)
            doc_handler_log.info(f'successful transcoding {self.output_dir}/{file_out} {process.communicate()}')
        except subprocess.TimeoutExpired:
            self.__kill_process(process)
            doc_handler_log.info('timeout expired')
            return None
        try:
            with open(f'{self.output_dir}/{file_out}', "rt") as file:
                file_content = file.read()
            self.clear_temp_file(f'{self.output_dir}/{file_out}')
            return file_content
        except FileNotFoundError:
            doc_handler_log.info(f'File not Found {self.output_dir}/{file_out}')
            return None

'''

