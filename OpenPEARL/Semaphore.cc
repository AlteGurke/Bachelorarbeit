/*
 [The "BSD license"]
 Copyright (c) 2012-2013 Rainer Mueller
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
 3. The name of the author may not be used to endorse or promote products
    derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

/**
\file

\brief semaphore implementation for posix threads using simultaneous
locking pattern

*/

#define __STDC_LIMIT_MACROS   // enable UINT32_MAX-macro
// must be set before stdint.h
#include <stdint.h>
#include "TaskCommon.h"
#include "Semaphore.h"
#include "Log.h"
#include "lockTracer/LockTracer.h"
#include "lockTracer/LockTraceEntry.h"

namespace pearlrt {

   PriorityQueue Semaphore::waiters;

   Semaphore::Semaphore(uint32_t preset, const char * n) {
      value = preset;
      name = n;
      Log::debug("Sema %s created with preset %u", n, (int)preset);
   }

   const char * Semaphore::getName(void) {
      return name;
   }

   uint32_t Semaphore::getValue(void) {
      return value;
   }

   void Semaphore::decrement(void) {
      value --;
   }

   void Semaphore::increment(void) {
      if (value == UINT32_MAX) {
         throw theSemaOverflowSignal;
      }

      value ++;
   }

   int Semaphore::check(BlockData::BlockReasons::BlockSema *bd) {
      int wouldBlock = 0;
      int i;

      for (i = 0; i < bd->nsemas; i++) {
         if (bd->semas[i]->getValue() == 0) {
            wouldBlock = 1;
         }

         Log::debug("   check::sema: %s is %d",
                    bd->semas[i]->getName(), (int)bd->semas[i]->getValue());
      }

      return wouldBlock;
   }

   void TraceLock(char* tName, const char* semaName) {
      LockTracer& lockTracer = LockTracer::GetInstance();
      if(lockTracer.IsEnabled() == false) {
         return;
      }

      LockTraceEntry entry = LockTraceEntry(std::chrono::high_resolution_clock::now(), LockTraceEntryType::Lock, tName, semaName);
      lockTracer.Add(entry);
   }

   void TraceUnlock(char* tName, const char* semaName) {
      LockTracer& lockTracer = LockTracer::GetInstance();
      if(lockTracer.IsEnabled() == false) {
         return;
      }

      LockTraceEntry entry = LockTraceEntry(std::chrono::high_resolution_clock::now(), LockTraceEntryType::Unlock, tName, semaName);
      lockTracer.Add(entry);
   }

   void Semaphore::request(TaskCommon* me,
                           int nbrOfSemas,
                           Semaphore** semas) {
      int i;
      int wouldBlock = 0;
      BlockData bd;

      bd.reason = REQUEST;
      bd.u.sema.nsemas = nbrOfSemas;
      bd.u.sema.semas = semas;

      TaskCommon::mutexLock();
      Log::info("request from task %s for %d semaphores", me->getName(),
                nbrOfSemas);

      wouldBlock = check(&(bd.u.sema));

      if (! wouldBlock) {
         for (i = 0; i < nbrOfSemas; i++) {
            semas[i]->decrement();
            if (semas[i]->getValue() == 0) {
               TraceLock(me->getName(), semas[i]->getName());
            }
         }

         // critival region end
         TaskCommon::mutexUnlock();
      } else {
         Log::info("   task: %s going to blocked", me->getName());
         waiters.insert(me);
         // critical region ends in block()
         me->block(&bd);
         me->scheduleCallback();
      }
   }

   void Semaphore::release(TaskCommon* me,
                           int nbrOfSemas,
                           Semaphore** semas) {
      BlockData bd;
      int i;
      int wouldBlock;

      // start critical region - end after doinf all possible releases
      TaskCommon::mutexLock();
      Log::debug("release from task %s for %d semaphores", me->getName(),
                 nbrOfSemas);

      try {
         for (i = 0; i < nbrOfSemas; i++) {
            semas[i]->increment();
            if (semas[i]->getValue() == 1) {
               TraceUnlock(me->getName(), semas[i]->getName());
            }
            Log::debug("   sema: %s is now %u",
                       semas[i]->getName(), (int)semas[i]->getValue());
         }
      } catch (SemaOverflowSignal x) {
         Log::error("SemaOverflowSignal for %s",
                    semas[i]->getName());
         TaskCommon::mutexUnlock();
         throw;
      }

      TaskCommon * t = waiters.getHead();;

      while (t != 0) {
         t->getBlockingRequest(&bd);
         wouldBlock = check(&(bd.u.sema));

         if (!wouldBlock)  {
            for (i = 0; i < bd.u.sema.nsemas; i++) {
               bd.u.sema.semas[i]->decrement();
               if (bd.u.sema.semas[i]->getValue() == 0) {
                  TraceLock(me->getName(), bd.u.sema.semas[i]->getName());
               }
            }

            waiters.remove(t);
            t->unblock();
            Log::info("   unblocking: %s", t->getName());
         } else {
            Log::debug("   task %s still blocked", t->getName());
         }

         t = waiters.getNext(t);
      }

      TaskCommon::mutexUnlock();
   }

   BitString<1> Semaphore::dotry(TaskCommon* me,  int nbrOfSemas, Semaphore** semas) {
      int i;
      int wouldBlock = 0;
      BlockData bd;
      BitString<1> result(1);  // true

      bd.reason = REQUEST;
      bd.u.sema.nsemas = nbrOfSemas;
      bd.u.sema.semas = semas;

      // start critical region
      TaskCommon::mutexLock();
      Log::debug("try from task %s for %d semaphores", me->getName(),
                 nbrOfSemas);
      wouldBlock = check(&(bd.u.sema));

      if (! wouldBlock) {
         for (i = 0; i < nbrOfSemas; i++) {
            semas[i]->decrement();
            if (semas[i]->getValue() == 0) {
               TraceLock(me->getName(), semas[i]->getName());
            }
         }
      }

      TaskCommon::mutexUnlock();

      if (wouldBlock) {
         result.x = 0;   // false
      }

      //return !wouldBlock;
      return result;
   }

   void Semaphore::removeFromWaitQueue(TaskCommon * t) {
      waiters.remove(t);
   }

   void Semaphore::addToWaitQueue(TaskCommon * t) {
      BlockData bd;
      int wouldBlock;

      t->getBlockingRequest(&bd);
      wouldBlock = check(&(bd.u.sema));

      if (!wouldBlock)  {
         for (int i = 0; i < bd.u.sema.nsemas; i++) {
            bd.u.sema.semas[i]->decrement();
            if (bd.u.sema.semas[i]->getValue() == 0) {
               TraceLock(t->getName(), bd.u.sema.semas[i]->getName());
            }
            
         }

         waiters.remove(t);
         t->unblock();
         Log::debug("   unblocking: %s", t->getName());
      }  else {
         waiters.insert(t);
      }

   }

   void Semaphore::updateWaitQueue(TaskCommon * t) {
      if (waiters.remove(t)) {
         waiters.insert(t);
      }
   }
}
